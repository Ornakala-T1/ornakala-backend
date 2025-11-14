#!/bin/bash

# Ornakala Backend Deployment Script
# Usage: ./deploy.sh [dev|prod] [image_tag]

set -e  # Exit on any error

ENVIRONMENT=$1
IMAGE_TAG=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$IMAGE_TAG" ]; then
    echo "Usage: ./deploy.sh [dev|prod] [image_tag]"
    exit 1
fi

echo "🚀 Starting deployment to $ENVIRONMENT environment with image tag: $IMAGE_TAG"

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose -f docker-compose.$ENVIRONMENT.yml down --remove-orphans || true

# Load new Docker image
echo "📥 Loading new Docker image..."
gunzip -c ornakala-backend.tar.gz | docker load

# Tag the image appropriately
docker tag ornakala-backend:$IMAGE_TAG ornakala-backend:latest

# Start new containers
echo "🔄 Starting new containers..."
docker-compose -f docker-compose.$ENVIRONMENT.yml up -d

# Wait for application to be ready
echo "⏳ Waiting for application to be ready..."
sleep 30

# Health check
echo "🔍 Performing health check..."
if [ "$ENVIRONMENT" = "prod" ]; then
    HEALTH_URL="http://be-pr.ornakala.com/health"
else
    HEALTH_URL="http://be-de.ornakala.com/health"
fi

for i in {1..10}; do
    if curl -f $HEALTH_URL > /dev/null 2>&1; then
        echo "✅ Health check passed!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Health check failed after 10 attempts"
        exit 1
    fi
    echo "🔄 Health check attempt $i failed, retrying in 10 seconds..."
    sleep 10
done

# Cleanup old images
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "🎉 Deployment to $ENVIRONMENT completed successfully!"

# Send notification (optional)
if [ "$ENVIRONMENT" = "prod" ]; then
    echo "📧 Sending deployment notification..."
    # Add your notification logic here (Slack, email, etc.)
fi