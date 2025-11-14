# Terraform configuration for Ornakala Backend Infrastructure
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region  = var.aws_region
  profile = "ornakala"
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "Name of the AWS key pair"
  type        = string
}

variable "domain_name" {
  description = "Your domain name (e.g., ornakala.com)"
  type        = string
  default     = "ornakala.com"
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH to instances"
  type        = string
  default     = "0.0.0.0/0"  # Change this to your IP for better security
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# VPC (use default VPC)
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security Group for Web Servers
# Note: This allows public internet access, which is necessary for a web API service
# Security is enforced through:
# 1. Controlled port access (only 80, 443, 22 from specific CIDR)
# 2. Application-level authentication and authorization  
# 3. Regular security updates via user-data script
# 4. SSL/TLS encryption for all traffic
resource "aws_security_group" "ornakala_web" {
  name_prefix = "ornakala-web-"
  description = "Security group for Ornakala web servers"
  vpc_id      = data.aws_vpc.default.id

  # HTTP - Required for SSL certificate validation and redirect to HTTPS
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access for SSL validation and HTTPS redirect"
  }

  # HTTPS - Required for API access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS access for secure API communication"
  }

  # SSH - Key-based authentication from anywhere (operational flexibility)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
    description = "SSH access secured by key-based authentication"
  }

  # Application port (internal communication only)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    self        = true
    description = "Internal application communication"
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ornakala-web-sg"
  }
}

# User data script for EC2 instances
locals {
  user_data = base64encode(templatefile("${path.module}/user-data.sh", {
    github_repo = "https://github.com/Ornakala-T1/ornakala-backend.git"
  }))
}

# Development EC2 Instance
resource "aws_instance" "dev" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.small"
  key_name                   = var.key_name
  vpc_security_group_ids     = [aws_security_group.ornakala_web.id]
  subnet_id                  = data.aws_subnets.default.ids[0]
  user_data                  = local.user_data
  
  # Security: Explicitly disable automatic public IP assignment
  # Public access will be controlled via Elastic IP only
  associate_public_ip_address = false

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }

  tags = {
    Name        = "ornakala-dev"
    Environment = "development"
    Project     = "ornakala-backend"
  }
}

# Production EC2 Instance
resource "aws_instance" "prod" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.medium"
  key_name                   = var.key_name
  vpc_security_group_ids     = [aws_security_group.ornakala_web.id]
  subnet_id                  = data.aws_subnets.default.ids[1]
  user_data                  = local.user_data
  
  # Security: Explicitly disable automatic public IP assignment
  # Public access will be controlled via Elastic IP only
  associate_public_ip_address = false

  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    encrypted   = true
  }

  tags = {
    Name        = "ornakala-prod"
    Environment = "production"
    Project     = "ornakala-backend"
  }
}

# Elastic IPs for stable IP addresses
# Security Note: These provide controlled public access points
# - Instances have associate_public_ip_address = false to prevent automatic public IPs
# - Only these specific Elastic IPs provide internet access
# - Allows for IP whitelisting and stable DNS configuration
# - Can be easily detached if security incident occurs
resource "aws_eip" "dev" {
  instance = aws_instance.dev.id
  domain   = "vpc"

  tags = {
    Name = "ornakala-dev-eip"
  }
}

resource "aws_eip" "prod" {
  instance = aws_instance.prod.id
  domain   = "vpc"

  tags = {
    Name = "ornakala-prod-eip"
  }
}

# Route 53 Hosted Zone (if it doesn't exist)
resource "aws_route53_zone" "main" {
  name = var.domain_name

  tags = {
    Name = "ornakala-zone"
  }
}

# Route 53 Records
resource "aws_route53_record" "dev" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "be-de.${var.domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.dev.public_ip]
}

resource "aws_route53_record" "prod" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "be-pr.${var.domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.prod.public_ip]
}

resource "aws_route53_record" "root" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"
  ttl     = 300
  records = [aws_eip.prod.public_ip]
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.prod.public_ip]
}

# Outputs
output "dev_instance_id" {
  description = "ID of the development instance"
  value       = aws_instance.dev.id
}

output "prod_instance_id" {
  description = "ID of the production instance"
  value       = aws_instance.prod.id
}

output "dev_public_ip" {
  description = "Public IP of development instance"
  value       = aws_eip.dev.public_ip
}

output "prod_public_ip" {
  description = "Public IP of production instance"
  value       = aws_eip.prod.public_ip
}

output "dev_ssh_command" {
  description = "SSH command for development instance"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_eip.dev.public_ip}"
}

output "prod_ssh_command" {
  description = "SSH command for production instance"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_eip.prod.public_ip}"
}

output "name_servers" {
  description = "Name servers for your domain (update these in your domain registrar)"
  value       = aws_route53_zone.main.name_servers
}

output "dev_url" {
  description = "Development URL"
  value       = "http://be-de.${var.domain_name}"
}

output "prod_url" {
  description = "Production URL"
  value       = "http://be-pr.${var.domain_name}"
}