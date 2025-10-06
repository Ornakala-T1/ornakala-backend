#!/bin/bash

# Database backup script for production
set -e

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
RETENTION_DAYS=30

echo "🗃️  Starting database backup at $(date)"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform backup
pg_dump -h postgres -U $POSTGRES_USER -d $POSTGRES_DB > $BACKUP_DIR/ornakala_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/ornakala_backup_$DATE.sql

echo "✅ Backup completed: ornakala_backup_$DATE.sql.gz"

# Clean up old backups (keep only last 30 days)
find $BACKUP_DIR -name "ornakala_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "🧹 Cleaned up backups older than $RETENTION_DAYS days"

# Optional: Upload to S3
# aws s3 cp $BACKUP_DIR/ornakala_backup_$DATE.sql.gz s3://your-backup-bucket/

echo "🎉 Backup process completed successfully!"