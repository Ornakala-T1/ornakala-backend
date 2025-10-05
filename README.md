# Ornakala Backend

The **Ornakala Backend** powers the **customer-facing side** of the Ornakala platform — an AI-powered jewelry discovery and personalization ecosystem.  
It provides secure REST APIs for mobile and web clients, enabling users to browse jewelry collections, try them on using AR, receive AI-generated design recommendations, and place custom or ready-made orders.

---

## 🧭 Overview

This backend focuses exclusively on **customers** (not vendors or manufacturers).  
It manages:
- 🧍 User registration, authentication, and profiles  
- 💍 Jewelry catalog browsing and search  
- 🤖 AI-powered design recommendations and personalization  
- 🪄 Augmented Reality (AR) try-on integration  
- 🛒 Cart, checkout, and order tracking  
- 🔔 Notifications and order status updates  

Vendor and production-side APIs are maintained separately in the [`ornakala-vendor-backend`](https://github.com/ornakala/ornakala-vendor-backend) repository.

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
git clone https://github.com/ornakala/ornakala-backend.git
cd ornakala-backend
