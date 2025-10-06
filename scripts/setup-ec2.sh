#!/bin/bash

# EC2 Instance Setup Script for Ornakala Backend
# Run this script on your EC2 instances to prepare them for deployment

set -e

echo "🛠️  Setting up EC2 instance for Ornakala Backend..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Install additional tools
echo "🔧 Installing additional tools..."
sudo apt-get install -y htop nginx certbot python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
mkdir -p /home/$USER/ornakala-backend
cd /home/$USER/ornakala-backend

# Create logs directory
mkdir -p logs

# Set up log rotation
echo "📄 Setting up log rotation..."
sudo tee /etc/logrotate.d/ornakala-backend > /dev/null << EOF
/home/$USER/ornakala-backend/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Create systemd service for monitoring
echo "📊 Creating monitoring service..."
sudo tee /etc/systemd/system/ornakala-monitor.service > /dev/null << EOF
[Unit]
Description=Ornakala Backend Monitor
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=$USER
ExecStart=/bin/bash -c 'docker-compose -f /home/$USER/docker-compose.\$(cat /home/$USER/.env | grep ENVIRONMENT | cut -d= -f2).yml ps'

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable ornakala-monitor.service

echo "✅ EC2 instance setup completed!"
echo "📝 Next steps:"
echo "1. Configure your environment variables in .env file"
echo "2. Set up SSL certificates"
echo "3. Configure domain DNS"
echo "4. Test deployment"

echo "💡 Don't forget to reboot to apply docker group changes!"