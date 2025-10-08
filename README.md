# Ornakala Backend

The **Ornakala Backend** powers the **customer-facing side** of the Ornakala platform — an AI-powered jewelry discovery and personalization ecosystem.  
It provides secure REST APIs for mobile and web clients, enabling users to browse jewelry collections, try them on using AR, receive AI-generated design recommendations, and place custom or ready-made orders.

---

## 🧭 Overview

This backend focuses exclusively on **customers**, **vendors** or **manufacturers**.  
It manages:
- 🧍 User registration, authentication, and profiles  
- 💍 Jewelry catalog browsing and search  
- 🤖 AI-powered design recommendations and personalization  
- 🪄 Augmented Reality (AR) try-on integration  
- 🛒 Cart, checkout, and order tracking  
- 🔔 Notifications and order status updates  

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend Framework | **FastAPI** (Python 3.11+) |
| Database | **MySQL / PostgreSQL** |
| Authentication | JWT-based Auth with Role Management |
| AI Services | Ornakala AI Engine (design recommendations, similarity search) |
| Storage | AWS S3 / Cloud Storage for images & models |
| CI/CD | GitHub Actions + SonarQube Quality Gate |
| Infrastructure | Docker / AWS ECS / GCP Cloud Run |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Ornakala-T1/ornakala-backend.git
cd ornakala-backend
```

### 2️⃣ Install dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3️⃣ Run tests
```bash
# Run all tests with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py -v

# Run tests with coverage threshold
pytest tests/ --cov=. --cov-fail-under=80
```

### 4️⃣ Code quality checks
```bash
# Linting with Ruff
ruff check .

# Format code with Ruff
ruff format .

# Type checking with MyPy
mypy .
```

---

## 🧪 Testing

The project uses **pytest** for testing with the following structure:

```
tests/
├── __init__.py
├── test_main.py           # Main application tests
└── test_script_execution.py  # Script execution tests
```

### Test Coverage Requirements
- **Minimum coverage**: 80%
- **Coverage reports**: HTML and XML formats
- **SonarQube integration**: Quality gate enforcement

### Running Tests Locally
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## 🚀 Deployment & Infrastructure

### Live Environments
- **Development**: https://be-de.ornakala.com (auto-deploy on `main`)
- **Production**: https://be-pr.ornakala.com (manual deployment)

### Automated Deployment Process
1. **Code Push**: Push/merge to `main` branch (only `arijitaich` can push to main)
2. **Quality Gate**: SonarQube scan and tests must pass
3. **Auto-Deploy**: Automatically deploys to development server
4. **Process Management**: Stops existing `main.py` and starts new version
5. **Verification**: Confirms `main.py` is running successfully

### Infrastructure
- **AWS EC2**: t3.small (dev) + t3.medium (prod)
- **DNS**: Route53 with custom domains
- **SSL**: Comodo/Sectigo certificates
- **CI/CD**: GitHub Actions with automated testing and deployment
- **Process**: Direct Python execution with process management

### Manual Server Management
Use the management script for manual control:
```bash
# SSH to dev server
ssh -i ornakala-keypair-fixed.pem ubuntu@3.143.178.63

# Use management script
cd ~/ornakala-backend
chmod +x scripts/manage.sh

# Available commands
./scripts/manage.sh status    # Check if main.py is running
./scripts/manage.sh logs      # View recent logs
./scripts/manage.sh restart   # Restart main.py
./scripts/manage.sh stop      # Stop main.py
./scripts/manage.sh start     # Start main.py
```

### Deployment
1. **Auto-deploy**: Push to `main` branch → deploys to development
2. **Production**: Manual trigger via GitHub Actions
3. **Full Guide**: See [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)

### Frontend Integration
- **Separate Repository**: Frontend will be in its own repository
- **API Endpoints**: Backend provides REST APIs at the above URLs
- **CORS**: Configured to allow cross-origin requests from frontend domains

### Security
- **Network**: Explicit public IP control with managed Elastic IPs
- **Access**: SSH secured by key-based authentication, application port internal-only  
- **Encryption**: SSL/TLS for all traffic, encrypted storage volumes
- **Authentication**: JWT-based API authentication (when implemented)
- **Branch Protection**: Only `arijitaich` can push/merge to main branch

---

## 📄 Documentation

- **[DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)**: Complete infrastructure and deployment guide
