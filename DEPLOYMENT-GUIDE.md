# Complete Frontend & Backend Deployment Guide

## Architecture Overview

Your Ornakala application now supports complete frontend/backend separation across dev/prod environments:

### Domain Structure
- **Backend Development**: `be-de.ornakala.com` → 3.143.178.63 (t3.small)
- **Backend Production**: `be-pr.ornakala.com` → 3.146.137.204 (t3.medium)
- **Frontend Development**: `fe-de.ornakala.com` → 3.143.178.63 (same server as backend dev)
- **Frontend Production**: `www.ornakala.com` → 3.146.137.204 (same server as backend prod)
- **Root Domain**: `ornakala.com` → 3.146.137.204 (redirects to www)

## Current Status

### ✅ Completed
1. **AWS Infrastructure**: EC2 instances, Route53 DNS, Security Groups
2. **DNS Configuration**: All domains resolving correctly
3. **SSL Domain Verification**: File uploaded for BigRock/Comodo approval
4. **Backend CI/CD**: GitHub Actions workflow for automated deployment
5. **Frontend CI/CD**: Separate workflow for frontend deployment
6. **Nginx Configuration**: Ready for both frontend and backend serving

### ⏳ Pending
1. **SSL Certificate Approval**: Waiting for Comodo/Sectigo certificate
2. **SSL Certificate Update**: Need to include `fe-de.ornakala.com` subdomain
3. **Frontend Application**: React app development

## SSL Certificate Next Steps

### Current SSL Request
- Domain: `ornakala.com`
- Subdomains: `be-de.ornakala.com`, `be-pr.ornakala.com`, `www.ornakala.com`
- Missing: `fe-de.ornakala.com`

### Action Required
Once your current SSL certificate is approved:
1. **Reissue certificate** to include `fe-de.ornakala.com`
2. **Update certificate** on both servers
3. **Test all domains** with HTTPS

## Deployment Workflows

### Backend Deployment
- **Trigger**: Push to `main` branch
- **Auto-deploy**: Development environment
- **Manual deploy**: Production (after testing)
- **Pipeline**: Tests → Build → Deploy → Notify

### Frontend Deployment
- **Trigger**: Push to `main` branch (with `frontend/` changes)
- **Auto-deploy**: Development environment
- **Manual deploy**: Production
- **Pipeline**: Build → Test → Deploy → Notify

## Directory Structure

```
ornakala-backend/
├── frontend/                    # React application
│   ├── package.json            # Dependencies & build scripts
│   ├── .env.development        # Dev environment config
│   ├── .env.production         # Prod environment config
│   └── src/                    # React source code
├── .github/workflows/
│   ├── deploy.yml              # Backend CI/CD
│   └── deploy-frontend.yml     # Frontend CI/CD
├── scripts/
│   ├── deploy.sh               # Backend deployment script
│   └── deploy-frontend.sh      # Frontend deployment script
├── nginx/
│   └── nginx.conf              # Complete nginx config
└── infrastructure/
    └── main.tf                 # Terraform AWS infrastructure
```

## Server Configuration

### Development Server (3.143.178.63)
- **Backend API**: Port 8000 → `be-de.ornakala.com`
- **Frontend App**: `/var/www/frontend` → `fe-de.ornakala.com`
- **Nginx**: Reverse proxy + static file serving

### Production Server (3.146.137.204)
- **Backend API**: Port 8000 → `be-pr.ornakala.com`, `ornakala.com`
- **Frontend App**: `/var/www/frontend-prod` → `www.ornakala.com`
- **Nginx**: Reverse proxy + static file serving

## Frontend Development Setup

1. **Create React App** (if not exists):
   ```bash
   cd frontend/
   npx create-react-app . --template typescript
   ```

2. **Install Dependencies**:
   ```bash
   npm install axios react-router-dom
   ```

3. **Configure API Base URL**:
   - Development: `https://be-de.ornakala.com`
   - Production: `https://be-pr.ornakala.com`

4. **Build Commands**:
   ```bash
   npm run build:dev    # For development deployment
   npm run build:prod   # For production deployment
   ```

## Manual Deployment Commands

### Deploy Backend
```bash
# Development
git push origin main  # Auto-deploys to dev

# Production (manual)
# Go to GitHub Actions → Run workflow → Select "prod"
```

### Deploy Frontend
```bash
# Development
git add frontend/
git commit -m "Update frontend"
git push origin main  # Auto-deploys frontend to dev

# Production (manual)
# Go to GitHub Actions → Frontend CI/CD → Run workflow → Select "prod"
```

## Testing Endpoints

Once SSL is configured, test these URLs:

### Development
- **Backend API**: `https://be-de.ornakala.com/health`
- **Frontend App**: `https://fe-de.ornakala.com`

### Production
- **Backend API**: `https://be-pr.ornakala.com/health`
- **Frontend App**: `https://www.ornakala.com`
- **Root Domain**: `https://ornakala.com` (should redirect)

## Monitoring & Logs

### Server Access
```bash
# Development server
ssh -i ornakala-keypair-fixed.pem ubuntu@3.143.178.63

# Production server
ssh -i ornakala-keypair-fixed.pem ubuntu@3.146.137.204
```

### Log Locations
- **Nginx Logs**: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- **Backend Logs**: Check your application logs
- **Deployment Logs**: `/var/log/frontend-deployments.log`

## Security Features

- **HTTPS Only**: All traffic redirected to SSL
- **CORS Configuration**: Frontend domains whitelisted
- **Security Groups**: Only required ports open (22, 80, 443)
- **Encrypted Storage**: EBS volumes encrypted

## Next Steps

1. **Wait for SSL approval** from Comodo/Sectigo
2. **Update SSL certificate** to include `fe-de.ornakala.com`
3. **Deploy nginx configuration** to both servers
4. **Create React frontend application**
5. **Test complete deployment pipeline**

## Support

All infrastructure is now ready for your complete frontend/backend architecture. The DNS, CI/CD pipelines, and deployment scripts are configured and waiting for SSL certificate approval to go live.