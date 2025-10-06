# Custom SSL Setup Guide for Ornakala Domains

## Domain Structure
- **Production**: `be-pr.ornakala.com`
- **Development**: `be-de.ornakala.com`
- **Main Site**: `ornakala.com` and `www.ornakala.com`

## SSL Certificate Setup

### Step 1: Prepare Your SSL Certificate Files
You'll need these files for your ornakala.com domain:
- `ornakala.com.crt` - Your SSL certificate
- `ornakala.com.key` - Your private key
- `ornakala.com.ca-bundle` - Intermediate certificates (if provided)

### Step 2: Create Full Chain Certificate
```bash
# Combine your certificate with the CA bundle
cat ornakala.com.crt ornakala.com.ca-bundle > ornakala.com.fullchain.crt
```

### Step 3: Upload Certificates to Both EC2 Instances

#### For Production Server (be-pr.ornakala.com):
```bash
# SSH into production server
ssh -i your-key.pem ubuntu@be-pr.ornakala.com

# Create SSL directory
sudo mkdir -p /etc/ssl/certs

# Copy certificate files (you'll need to upload these first)
sudo cp ornakala.com.crt /etc/ssl/certs/
sudo cp ornakala.com.key /etc/ssl/certs/
sudo cp ornakala.com.ca-bundle /etc/ssl/certs/

# Create full chain
sudo cat /etc/ssl/certs/ornakala.com.crt /etc/ssl/certs/ornakala.com.ca-bundle > /etc/ssl/certs/ornakala.com.fullchain.crt

# Set proper permissions
sudo chmod 644 /etc/ssl/certs/ornakala.com*.crt
sudo chmod 600 /etc/ssl/certs/ornakala.com.key
sudo chown root:root /etc/ssl/certs/ornakala.com*
```

#### For Development Server (be-de.ornakala.com):
If you have a separate certificate for the development subdomain:
```bash
# SSH into development server
ssh -i your-key.pem ubuntu@be-de.ornakala.com

# Create SSL directory
sudo mkdir -p /etc/ssl/certs

# If using the same wildcard certificate
sudo cp ornakala.com.crt /etc/ssl/certs/be-de.ornakala.com.crt
sudo cp ornakala.com.key /etc/ssl/certs/be-de.ornakala.com.key

# Set permissions
sudo chmod 644 /etc/ssl/certs/be-de.ornakala.com.crt
sudo chmod 600 /etc/ssl/certs/be-de.ornakala.com.key
sudo chown root:root /etc/ssl/certs/be-de.ornakala.com*
```

### Step 4: DNS Configuration
In your domain registrar or DNS provider, create these records:

```
# A Records (point to your EC2 Elastic IPs or ALB)
be-pr.ornakala.com    A    [Your Production Server IP]
be-de.ornakala.com    A    [Your Development Server IP]
ornakala.com          A    [Your Main Server IP]
www.ornakala.com      A    [Your Main Server IP]

# Or CNAME Records (if using Application Load Balancer)
be-pr.ornakala.com    CNAME    your-alb-name.region.elb.amazonaws.com
be-de.ornakala.com    CNAME    your-alb-name.region.elb.amazonaws.com
```

### Step 5: GitHub Secrets Configuration
Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
EC2_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
[your EC2 private key content]
-----END RSA PRIVATE KEY-----
EC2_DEV_HOST=be-de.ornakala.com
EC2_DEV_USER=ubuntu
EC2_PROD_HOST=be-pr.ornakala.com
EC2_PROD_USER=ubuntu
SONAR_TOKEN=your-sonarqube-token
```

### Step 6: Verify SSL Configuration
After deploying, test your SSL setup:

```bash
# Test production
curl -I https://be-pr.ornakala.com/health

# Test development
curl -I https://be-de.ornakala.com/health

# Check certificate details
openssl s_client -connect be-pr.ornakala.com:443 -servername be-pr.ornakala.com
```

## Important Notes

1. **Wildcard Certificate**: If you have a wildcard certificate (*.ornakala.com), you can use the same certificate for both subdomains.

2. **Certificate Renewal**: Since you're using custom SSL certificates, you'll need to manually renew them before expiration and update the files on your servers.

3. **Security**: Always keep your private key secure and never commit it to version control.

4. **Load Balancer**: If using AWS Application Load Balancer, you can upload your certificate to AWS Certificate Manager (ACM) instead of installing it on individual EC2 instances.

## ALB with Custom SSL (Recommended)

If you prefer to use Application Load Balancer with your custom SSL:

```bash
# Upload certificate to ACM
aws acm import-certificate \
    --certificate fileb://ornakala.com.crt \
    --private-key fileb://ornakala.com.key \
    --certificate-chain fileb://ornakala.com.ca-bundle \
    --region us-east-1
```

This approach centralizes SSL termination at the load balancer level and is more scalable.

## Deployment Workflow

1. **Code Push** → GitHub Actions runs tests → SonarQube check
2. **Dev Deployment** → Automatic deployment to `be-de.ornakala.com`
3. **Prod Deployment** → Manual trigger → Deployment to `be-pr.ornakala.com`

Your infrastructure is now configured for your custom domain structure with your own SSL certificates!