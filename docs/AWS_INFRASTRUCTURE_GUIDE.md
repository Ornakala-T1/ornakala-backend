# AWS Infrastructure Setup Guide for Ornakala Backend

## Overview
This guide will help you set up a complete AWS infrastructure for your Ornakala backend with:
- 2 EC2 instances (dev and prod)
- Application Load Balancer
- Security Groups
- Auto Scaling (optional)
- Domain configuration
- SSL certificates

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Domain `ornakala.com` with access to DNS settings
- SSL certificate files

## Step 1: Create Security Groups

### 1.1 Web Security Group
```bash
aws ec2 create-security-group \
    --group-name ornakala-web-sg \
    --description "Security group for Ornakala web servers" \
    --vpc-id vpc-xxxxxxxxx  # Replace with your VPC ID
```

Add rules:
```bash
# HTTP
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# HTTPS
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# SSH (restrict to your IP)
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 22 \
    --cidr YOUR-IP-ADDRESS/32

# Application port (internal only)
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 8000 \
    --source-group sg-xxxxxxxxx
```

### 1.2 Database Security Group
```bash
aws ec2 create-security-group \
    --group-name ornakala-db-sg \
    --description "Security group for Ornakala database" \
    --vpc-id vpc-xxxxxxxxx

# PostgreSQL
aws ec2 authorize-security-group-ingress \
    --group-id sg-yyyyyyyyy \
    --protocol tcp \
    --port 5432 \
    --source-group sg-xxxxxxxxx  # Only from web servers

# Redis
aws ec2 authorize-security-group-ingress \
    --group-id sg-yyyyyyyyy \
    --protocol tcp \
    --port 6379 \
    --source-group sg-xxxxxxxxx
```

## Step 2: Launch EC2 Instances

### 2.1 Development Server
```bash
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1d0 \  # Ubuntu 22.04 LTS (update as needed)
    --count 1 \
    --instance-type t3.small \
    --key-name ornakala-keypair \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-xxxxxxxxx \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ornakala-dev},{Key=Environment,Value=development}]' \
    --user-data file://scripts/setup-ec2.sh
```

### 2.2 Production Server
```bash
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1d0 \
    --count 1 \
    --instance-type t3.medium \  # Larger for production
    --key-name ornakala-keypair \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-yyyyyyyyy \  # Different AZ for resilience
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ornakala-prod},{Key=Environment,Value=production}]' \
    --user-data file://scripts/setup-ec2.sh
```

## Step 3: Create Application Load Balancer

### 3.1 Create Target Groups
```bash
# Development target group
aws elbv2 create-target-group \
    --name ornakala-dev-tg \
    --protocol HTTP \
    --port 80 \
    --vpc-id vpc-xxxxxxxxx \
    --health-check-path /health \
    --health-check-interval-seconds 30 \
    --health-check-timeout-seconds 10 \
    --healthy-threshold-count 3 \
    --unhealthy-threshold-count 3

# Production target group
aws elbv2 create-target-group \
    --name ornakala-prod-tg \
    --protocol HTTP \
    --port 80 \
    --vpc-id vpc-xxxxxxxxx \
    --health-check-path /health
```

### 3.2 Create Load Balancer
```bash
aws elbv2 create-load-balancer \
    --name ornakala-alb \
    --subnets subnet-xxxxxxxxx subnet-yyyyyyyyy \
    --security-groups sg-xxxxxxxxx \
    --scheme internet-facing \
    --type application \
    --tags Key=Name,Value=ornakala-alb
```

### 3.3 Register Targets
```bash
# Register dev instance
aws elbv2 register-targets \
    --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/ornakala-dev-tg/xxxxxxxxx \
    --targets Id=i-dev-instance-id

# Register prod instance
aws elbv2 register-targets \
    --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/ornakala-prod-tg/xxxxxxxxx \
    --targets Id=i-prod-instance-id
```

## Step 4: Configure DNS

### 4.1 Create Route 53 Hosted Zone (if not exists)
```bash
aws route53 create-hosted-zone \
    --name ornakala.com \
    --caller-reference $(date +%s)
```

### 4.2 Create DNS Records
Create a JSON file `dns-records.json`:
```json
{
    "Comment": "Creating DNS records for Ornakala",
    "Changes": [
        {
            "Action": "CREATE",
            "ResourceRecordSet": {
                "Name": "api.ornakala.com",
                "Type": "A",
                "AliasTarget": {
                    "DNSName": "ornakala-alb-xxxxxxxxx.us-east-1.elb.amazonaws.com",
                    "EvaluateTargetHealth": true,
                    "HostedZoneId": "Z35SXDOTRQ7X7K"
                }
            }
        },
        {
            "Action": "CREATE",
            "ResourceRecordSet": {
                "Name": "dev-api.ornakala.com",
                "Type": "A",
                "AliasTarget": {
                    "DNSName": "ornakala-alb-xxxxxxxxx.us-east-1.elb.amazonaws.com",
                    "EvaluateTargetHealth": true,
                    "HostedZoneId": "Z35SXDOTRQ7X7K"
                }
            }
        }
    ]
}
```

Apply the changes:
```bash
aws route53 change-resource-record-sets \
    --hosted-zone-id Z1D633PJN98FT9 \
    --change-batch file://dns-records.json
```

## Step 5: Instance Configuration

### 5.1 Connect to Development Instance
```bash
ssh -i ornakala-keypair.pem ubuntu@be-de.ornakala.com
```

### 5.2 Run Setup Script
```bash
chmod +x setup-ec2.sh
./setup-ec2.sh
```

### 5.3 Configure Environment Variables
```bash
# Copy template and fill values
cp .env.template .env
nano .env
```

### 5.4 Set Environment Indicator
```bash
echo "ENVIRONMENT=development" > .env
# For production instance: echo "ENVIRONMENT=production" > .env
```

## Step 6: GitHub Actions Secrets

Add these secrets to your GitHub repository:

### Required Secrets:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
EC2_PRIVATE_KEY=contents-of-your-pem-file
EC2_DEV_HOST=dev-api.ornakala.com
EC2_DEV_USER=ubuntu
EC2_PROD_HOST=api.ornakala.com
EC2_PROD_USER=ubuntu
SONAR_TOKEN=your-sonarqube-token
```

## Step 7: Auto Scaling (Optional)

### 7.1 Create Launch Template
```bash
aws ec2 create-launch-template \
    --launch-template-name ornakala-template \
    --launch-template-data '{
        "ImageId": "ami-0c55b159cbfafe1d0",
        "InstanceType": "t3.small",
        "KeyName": "ornakala-keypair",
        "SecurityGroupIds": ["sg-xxxxxxxxx"],
        "UserData": "base64-encoded-setup-script",
        "TagSpecifications": [{
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": "ornakala-auto"}]
        }]
    }'
```

### 7.2 Create Auto Scaling Group
```bash
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name ornakala-asg \
    --launch-template LaunchTemplateName=ornakala-template,Version=1 \
    --min-size 1 \
    --max-size 3 \
    --desired-capacity 2 \
    --target-group-arns arn:aws:elasticloadbalancing:region:account:targetgroup/ornakala-prod-tg/xxxxxxxxx \
    --vpc-zone-identifier "subnet-xxxxxxxxx,subnet-yyyyyyyyy"
```

## Step 8: Monitoring and Alerts

### 8.1 CloudWatch Alarms
```bash
# CPU Utilization
aws cloudwatch put-metric-alarm \
    --alarm-name ornakala-high-cpu \
    --alarm-description "High CPU utilization" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=InstanceId,Value=i-xxxxxxxxx \
    --evaluation-periods 2

# Disk Space
aws cloudwatch put-metric-alarm \
    --alarm-name ornakala-low-disk \
    --alarm-description "Low disk space" \
    --metric-name DiskSpaceUtilization \
    --namespace CWAgent \
    --statistic Average \
    --period 300 \
    --threshold 85 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1
```

## Step 9: Cost Optimization

### 9.1 Reserved Instances
Consider purchasing Reserved Instances for production workloads to save costs.

### 9.2 Scheduled Scaling
For development environment, consider shutting down outside business hours:
```bash
# Create scheduled action to stop dev instance at night
aws autoscaling put-scheduled-update-group-action \
    --auto-scaling-group-name ornakala-dev-asg \
    --scheduled-action-name stop-dev-nights \
    --recurrence "0 22 * * 1-5" \
    --desired-capacity 0 \
    --min-size 0 \
    --max-size 0
```

## Estimated Monthly Costs

### Development Environment:
- EC2 t3.small: ~$15/month
- ALB: ~$18/month
- Data transfer: ~$5/month
- **Total: ~$38/month**

### Production Environment:
- EC2 t3.medium: ~$30/month
- ALB: ~$18/month
- Data transfer: ~$10/month
- Backups (S3): ~$5/month
- **Total: ~$63/month**

**Combined: ~$101/month**

## Security Best Practices

1. **Regular Updates**: Set up automated security updates
2. **Backup Strategy**: Regular database backups to S3
3. **Access Control**: Use IAM roles instead of access keys where possible
4. **Monitoring**: Set up CloudTrail for API logging
5. **Encryption**: Enable EBS encryption and use HTTPS everywhere

## Troubleshooting

### Common Issues:
1. **503 Service Unavailable**: Check target group health
2. **Connection Timeout**: Verify security group rules
3. **DNS Not Resolving**: Check Route 53 configuration
4. **SSL Certificate Issues**: Verify certificate installation

### Useful Commands:
```bash
# Check instance status
aws ec2 describe-instances --instance-ids i-xxxxxxxxx

# Check target group health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:...

# View CloudWatch logs
aws logs describe-log-groups
aws logs get-log-events --log-group-name /aws/ec2/ornakala
```