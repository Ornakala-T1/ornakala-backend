# Complete Backend API Deployment Guide

## Architecture Overview

Your Ornakala backend provides REST APIs for frontend applications across dev/prod environments:

### Domain Structure
- **Backend Development**: `be-de.ornakala.com` → 3.143.178.63 (t3.small)
- **Backend Production**: `be-pr.ornakala.com` → 3.146.137.204 (t3.medium)
- **Root Domain**: `ornakala.com` → 3.146.137.204 (points to production API)

### Repository Separation
- **Backend Repository**: This repo (ornakala-backend) - API only
- **Frontend Repository**: Separate repo for React/web applications
- **Benefits**: Team separation, security isolation, independent deployments

## Current Status

### ✅ Completed
1. **AWS Infrastructure**: EC2 instances, Route53 DNS, Security Groups
2. **DNS Configuration**: Backend domains resolving correctly
3. **SSL Domain Verification**: File uploaded for BigRock/Comodo approval
4. **Backend CI/CD**: GitHub Actions workflow for automated deployment
5. **Nginx Configuration**: Ready for backend API serving with CORS

### ⏳ Pending
1. **SSL Certificate Approval**: Waiting for Comodo/Sectigo certificate
2. **Frontend Repository**: Separate repo setup for frontend team

## SSL Certificate Next Steps

### Current SSL Request
- Domain: `ornakala.com`
- Subdomains: `be-de.ornakala.com`, `be-pr.ornakala.com`, `www.ornakala.com`
- Status: Domain verification completed, awaiting certificate approval

### Action Required
Once your SSL certificate is approved:
1. **Install certificate** on both backend servers
2. **Test API endpoints** with HTTPS
3. **Configure frontend repository** to use these API endpoints

## Deployment Workflows

### Backend Deployment (This Repository)
- **Trigger**: Push to `main` branch
- **Auto-deploy**: Development environment
- **Manual deploy**: Production (after testing)
- **Pipeline**: Tests → Build → Deploy → Notify

### Frontend Deployment (Separate Repository)
- **Repository**: To be created separately
- **API Integration**: Will consume APIs from this backend
- **Domains**: Frontend team will manage their own domains/hosting
- **Benefits**: Independent deployments, team separation, security isolation

## Directory Structure

```
ornakala-backend/                # Backend Repository (This Repo)
├── .github/workflows/
│   └── deploy.yml              # Backend CI/CD only
├── scripts/
│   └── deploy.sh               # Backend deployment script
├── nginx/
│   └── nginx.conf              # Backend API nginx config
├── infrastructure/
│   └── main.tf                 # AWS infrastructure (backend domains)
├── main.py                     # FastAPI backend application
├── requirements.txt            # Python dependencies
└── tests/                      # Backend tests

ornakala-frontend/               # Frontend Repository (Separate)
├── .github/workflows/          # Frontend-specific CI/CD
├── src/                        # React/frontend source code
├── package.json                # Frontend dependencies
└── build/                      # Frontend build artifacts
```

## Server Configuration

### Development Server (3.143.178.63)
- **Backend API**: Port 8000 → `be-de.ornakala.com`
- **Nginx**: Reverse proxy with CORS for frontend integration

### Production Server (3.146.137.204)
- **Backend API**: Port 8000 → `be-pr.ornakala.com`, `ornakala.com`
- **Nginx**: Reverse proxy with CORS for frontend integration

## API Integration for Frontend

### API Endpoints
- **Development**: `https://be-de.ornakala.com`
- **Production**: `https://be-pr.ornakala.com`

### CORS Configuration
- **Development**: Allows all origins (`*`) for flexibility
- **Production**: Allows specific frontend domains for security

### Frontend Setup (Separate Repository)
Frontend developers should:
1. **Create separate repository** for frontend code
2. **Configure API base URLs**:
   - Dev: `https://be-de.ornakala.com`
   - Prod: `https://be-pr.ornakala.com`
3. **Set up their own CI/CD** for frontend deployment
4. **Manage their own domains** (e.g., www.ornakala.com for frontend)

## Manual Deployment Commands

### Deploy Backend (This Repository)
```bash
# Development
git push origin main  # Auto-deploys to dev

# Production (manual)
# Go to GitHub Actions → Run workflow → Select "prod"
```

### Frontend Integration (Separate Repository)
Frontend team will:
```bash
# Set up their own repository
git clone https://github.com/Ornakala-T1/ornakala-frontend.git

# Configure API endpoints in their code
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://be-pr.ornakala.com' 
  : 'https://be-de.ornakala.com';

# Deploy independently from backend
```

## Testing Endpoints

Once SSL is configured, test these backend API URLs:

### Development
- **Backend API**: `https://be-de.ornakala.com/health`
- **API Documentation**: `https://be-de.ornakala.com/docs`

### Production
- **Backend API**: `https://be-pr.ornakala.com/health`
- **API Documentation**: `https://be-pr.ornakala.com/docs`
- **Root Domain**: `https://ornakala.com` (also points to API)

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
2. **Install SSL certificate** on both backend servers
3. **Deploy nginx configuration** to both servers
4. **Create separate frontend repository** for the frontend team
5. **Test backend API endpoints** once SSL is active

## Support

Backend infrastructure is now ready for your API-only architecture. The DNS, CI/CD pipeline, and deployment scripts are configured and waiting for SSL certificate approval to go live. Frontend team can start planning their separate repository.