#!/bin/bash

# Frontend Deployment Script for Ornakala
# Usage: ./deploy-frontend.sh [dev|prod] [commit_sha]

set -e  # Exit on any error

ENVIRONMENT=$1
COMMIT_SHA=$2
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

if [ -z "$ENVIRONMENT" ] || [ -z "$COMMIT_SHA" ]; then
    echo "❌ Error: Missing required parameters"
    echo "Usage: $0 [dev|prod] [commit_sha]"
    exit 1
fi

echo "🚀 Starting frontend deployment for $ENVIRONMENT environment"
echo "📦 Commit SHA: $COMMIT_SHA"
echo "⏰ Timestamp: $TIMESTAMP"

# Set environment-specific variables
if [ "$ENVIRONMENT" = "dev" ]; then
    FRONTEND_DIR="/var/www/frontend"
    DOMAIN="fe-de.ornakala.com"
    BACKUP_DIR="/var/www/backups/frontend-dev"
elif [ "$ENVIRONMENT" = "prod" ]; then
    FRONTEND_DIR="/var/www/frontend-prod"
    DOMAIN="www.ornakala.com"
    BACKUP_DIR="/var/www/backups/frontend-prod"
else
    echo "❌ Error: Invalid environment. Use 'dev' or 'prod'"
    exit 1
fi

echo "📁 Frontend directory: $FRONTEND_DIR"
echo "🌐 Domain: $DOMAIN"

# Create directories if they don't exist
sudo mkdir -p "$FRONTEND_DIR"
sudo mkdir -p "$BACKUP_DIR"
sudo mkdir -p "/tmp/frontend-deploy"

# Backup current frontend if it exists
if [ -d "$FRONTEND_DIR" ] && [ "$(ls -A $FRONTEND_DIR)" ]; then
    echo "💾 Creating backup of current frontend..."
    sudo cp -r "$FRONTEND_DIR" "$BACKUP_DIR/backup-$TIMESTAMP"
    echo "✅ Backup created at: $BACKUP_DIR/backup-$TIMESTAMP"
fi

# Extract new frontend build
echo "📤 Extracting frontend build..."
cd /tmp/frontend-deploy
tar -xzf "/home/ubuntu/frontend-$COMMIT_SHA.tar.gz"

# Verify build contents
if [ ! -f "index.html" ]; then
    echo "❌ Error: Invalid frontend build - index.html not found"
    exit 1
fi

echo "✅ Frontend build verified"

# Deploy new frontend
echo "🔄 Deploying new frontend..."
sudo rm -rf "$FRONTEND_DIR"/*
sudo cp -r * "$FRONTEND_DIR/"

# Set proper permissions
sudo chown -R www-data:www-data "$FRONTEND_DIR"
sudo chmod -R 755 "$FRONTEND_DIR"

# Reload nginx configuration
echo "🔄 Reloading nginx..."
sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
    echo "✅ Nginx configuration reloaded"
else
    echo "❌ Error: Nginx configuration test failed"
    # Restore from backup if available
    if [ -d "$BACKUP_DIR/backup-$TIMESTAMP" ]; then
        echo "🔄 Restoring from backup..."
        sudo rm -rf "$FRONTEND_DIR"/*
        sudo cp -r "$BACKUP_DIR/backup-$TIMESTAMP"/* "$FRONTEND_DIR/"
        sudo systemctl reload nginx
    fi
    exit 1
fi

# Test deployment
echo "🧪 Testing deployment..."
sleep 5

# Check if the site is accessible
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" || echo "000")

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "000" ]; then
    echo "✅ Frontend deployment successful!"
    echo "🌐 Website accessible at: https://$DOMAIN"
    
    # Create deployment record
    echo "$TIMESTAMP|$COMMIT_SHA|$ENVIRONMENT|SUCCESS" | sudo tee -a "/var/log/frontend-deployments.log"
    
    # Cleanup old backups (keep last 5)
    cd "$BACKUP_DIR"
    sudo ls -t | tail -n +6 | sudo xargs rm -rf --
    
    # Cleanup deployment files
    rm -rf "/tmp/frontend-deploy"
    rm -f "/home/ubuntu/frontend-$COMMIT_SHA.tar.gz"
    
    echo "🎉 Frontend deployment completed successfully!"
    
else
    echo "❌ Error: Website not accessible (HTTP $HTTP_STATUS)"
    echo "🔄 Restoring from backup..."
    
    if [ -d "$BACKUP_DIR/backup-$TIMESTAMP" ]; then
        sudo rm -rf "$FRONTEND_DIR"/*
        sudo cp -r "$BACKUP_DIR/backup-$TIMESTAMP"/* "$FRONTEND_DIR/"
        sudo systemctl reload nginx
        echo "✅ Backup restored"
    fi
    
    echo "$TIMESTAMP|$COMMIT_SHA|$ENVIRONMENT|FAILED" | sudo tee -a "/var/log/frontend-deployments.log"
    exit 1
fi