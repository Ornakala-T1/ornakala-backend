# Ornakala Backend CI/CD Workflow Guide

## 🔄 **Workflow Overview**

This CI/CD pipeline implements a **proper branching strategy** with automatic dev deployment and manual production deployment after testing.

## 📊 **Pipeline Flow**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Developer     │    │    Repository    │    │   CI/CD Jobs    │
│                 │    │                  │    │                 │
│ 1. Create       │───▶│ Pull Request     │───▶│ ✅ Tests        │
│    Feature      │    │ to main          │    │ ✅ SonarQube    │
│    Branch       │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                 │
                                 ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    You Review   │    │   Merge to       │    │  Auto Deploy    │
│   & Merge PR    │───▶│   main branch    │───▶│  to DEV Server  │
│                 │    │                  │    │  be-de.ornakala │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Manual Test   │    │   Manual Prod    │    │   Deploy to     │
│   on DEV Server │───▶│   Deployment     │───▶│   PROD Server   │
│                 │    │   Trigger        │    │   be-pr.ornakala│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🎯 **Step-by-Step Process**

### **Step 1: Developer Workflow**
```bash
# Developer creates feature branch
git checkout -b feature/new-jewelry-api
git push origin feature/new-jewelry-api

# Creates Pull Request to main branch
# GitHub automatically runs: Tests + SonarQube Quality Gate
```

### **Step 2: Code Review & Merge**
- You review the Pull Request
- If approved, merge to `main` branch
- **Automatic trigger**: Deployment to DEV server (`be-de.ornakala.com`)

### **Step 3: Development Testing**
- Test the application on `https://be-de.ornakala.com`
- Verify all features work as expected
- Check API endpoints, database connections, etc.

### **Step 4: Production Deployment**
- Go to GitHub Actions tab
- Click "Run workflow" → Select "Deploy to Production"
- **Manual trigger**: Deployment to PROD server (`be-pr.ornakala.com`)

## 🔧 **GitHub Actions Jobs**

### **1. `test-and-quality` Job**
**Triggers**: Every PR + Every push to main
- ✅ Install dependencies
- ✅ Run pytest with coverage
- ✅ SonarQube quality gate check
- ❌ Blocks deployment if tests fail

### **2. `build` Job**
**Triggers**: Only on main branch merges + manual prod deployment
- 🐳 Build Docker image
- 📦 Create deployment artifact
- 💾 Store for 30 days

### **3. `deploy-dev` Job**
**Triggers**: Automatic on main branch push
- 🚀 Auto-deploy to `be-de.ornakala.com`
- 📋 Copy deployment files
- 🔄 Execute deployment script
- ✅ Health check verification

### **4. `deploy-prod` Job**
**Triggers**: Manual workflow dispatch only
- ⚠️ Warning about testing on dev first
- 🏗️ Fresh build for production
- 🚀 Deploy to `be-pr.ornakala.com`
- 🎉 Production success notification

## 🛡️ **Quality Gates**

### **SonarQube Checks (Block Deployment)**
- Code coverage threshold
- Security vulnerabilities
- Code smells and maintainability
- Duplicated code detection

### **Deployment Requirements**
- ✅ All tests must pass
- ✅ SonarQube quality gate must pass
- ✅ Only from main branch (dev)
- ✅ Manual approval (prod)

## 🌍 **Environment Details**

### **Development Environment**
- **URL**: `https://be-de.ornakala.com`
- **Purpose**: Testing merged features
- **Deployment**: Automatic on main merge
- **SSL**: Your custom certificate

### **Production Environment**
- **URL**: `https://be-pr.ornakala.com`
- **Purpose**: Live application
- **Deployment**: Manual trigger only
- **SSL**: Your custom certificate

## 🎮 **How to Use**

### **For Contributors:**
1. Create feature branch from `main`
2. Make changes and push
3. Create Pull Request to `main`
4. Wait for code review and merge

### **For You (Maintainer):**
1. Review Pull Requests
2. Merge approved PRs to `main`
3. Test automatically deployed code on DEV
4. Manually trigger production deployment when ready

### **Manual Production Deployment:**
1. Go to GitHub repository
2. Click "Actions" tab
3. Select "CI/CD Pipeline" workflow
4. Click "Run workflow" button
5. Select "prod" environment
6. Click "Run workflow"

## 📊 **Monitoring & Notifications**

### **GitHub Environments**
- **Development**: Shows deployment status and URL
- **Production**: Requires manual approval + shows live URL

### **Deployment Notifications**
- ✅ Success/failure status in GitHub
- 🔗 Direct links to deployed applications
- 📝 Deployment logs and health checks

## 🔐 **Security Features**

- **Environment Protection**: Production requires manual approval
- **SSH Key Management**: Secure server access
- **SSL Certificates**: Your custom certificates
- **Secrets Management**: AWS credentials and keys stored securely

## 🐛 **Troubleshooting**

### **If Dev Deployment Fails:**
1. Check GitHub Actions logs
2. SSH into dev server: `ssh ubuntu@be-de.ornakala.com`
3. Check Docker logs: `docker-compose logs`

### **If Production Deployment Fails:**
1. Check if dev deployment worked first
2. Verify all secrets are configured
3. Check production server health

### **Common Issues:**
- **SonarQube failure**: Fix code quality issues
- **Test failures**: Fix failing tests before merge
- **Connection issues**: Check EC2 security groups

## 📈 **Benefits of This Workflow**

1. **Quality Assurance**: Every change is tested before deployment
2. **Safe Releases**: Manual production control prevents accidents
3. **Fast Feedback**: Immediate dev deployment for testing
4. **Rollback Ready**: Easy to revert if issues found
5. **Audit Trail**: Complete deployment history in GitHub

This workflow ensures that your Ornakala backend maintains high quality while providing fast iteration cycles for development!