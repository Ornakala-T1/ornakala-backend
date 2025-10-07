#!/bin/bash

# User data script for EC2 instances
# This script runs when the instance first boots

set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Install additional tools
apt-get install -y htop nginx git awscli

# Create application directory
mkdir -p /home/ubuntu/ornakala-backend
chown ubuntu:ubuntu /home/ubuntu/ornakala-backend

# Create logs directory
mkdir -p /home/ubuntu/ornakala-backend/logs
chown ubuntu:ubuntu /home/ubuntu/ornakala-backend/logs

# Clone the repository
cd /home/ubuntu
git clone ${github_repo} ornakala-backend-repo
chown -R ubuntu:ubuntu ornakala-backend-repo

# Copy necessary files to application directory
cp -r ornakala-backend-repo/ornakala-backend/* /home/ubuntu/ornakala-backend/
chown -R ubuntu:ubuntu /home/ubuntu/ornakala-backend

# Set up log rotation
cat > /etc/logrotate.d/ornakala-backend << EOF
/home/ubuntu/ornakala-backend/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
EOF

# Configure firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

# Create systemd service for health monitoring
cat > /etc/systemd/system/ornakala-monitor.service << EOF
[Unit]
Description=Ornakala Backend Monitor
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=ubuntu
WorkingDirectory=/home/ubuntu/ornakala-backend
ExecStart=/bin/bash -c 'if [ -f .env ]; then ENV=\$(cat .env | grep ENVIRONMENT | cut -d= -f2); docker-compose -f docker-compose.\$ENV.yml ps; fi'

[Install]
WantedBy=multi-user.target
EOF

systemctl enable ornakala-monitor.service

# Create welcome message
cat > /home/ubuntu/README.md << EOF
# Ornakala Backend Server Setup Complete

## Next Steps:
1. Upload your SSL certificates
2. Configure environment variables
3. Deploy your application

## Useful Commands:
- Check Docker: docker --version
- Check logs: cd ornakala-backend && docker-compose logs
- Restart services: cd ornakala-backend && docker-compose restart

## Directories:
- Application: /home/ubuntu/ornakala-backend
- Repository: /home/ubuntu/ornakala-backend-repo
- Logs: /home/ubuntu/ornakala-backend/logs
EOF

chown ubuntu:ubuntu /home/ubuntu/README.md

# Signal completion
echo "EC2 setup completed at $(date)" > /home/ubuntu/setup-complete.log
chown ubuntu:ubuntu /home/ubuntu/setup-complete.log