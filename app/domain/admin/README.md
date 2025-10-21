# Ornakala Platform - Admin Panel

A production-grade admin platform for the Ornakala system, featuring dynamic form creation, role-based access control, and comprehensive data management.

## 🏗️ Architecture

### Backend (NestJS)
- **Authentication**: JWT-based auth with MFA support
- **Authorization**: Role-based access control (RBAC)
- **Form Builder**: Dynamic form creation and management
- **Schema Management**: Automatic database table generation
- **Data Management**: Generic CRUD operations for dynamic tables
- **Audit Logging**: Comprehensive activity tracking
- **Admin Interface**: Table exploration and management

### Frontend (Next.js)
- **Modern UI**: Built with Next.js 14, TypeScript, and Tailwind CSS
- **Form Builder**: Visual form designer
- **Data Management**: Table viewer and editor
- **User Management**: Admin and developer management
- **Dashboard**: Overview and quick actions

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- PostgreSQL 15+
- Redis (optional)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd app/domain/admin/backend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your database and JWT secrets
   ```

4. **Set up database:**
   ```bash
   # Generate Prisma client
   npm run prisma:generate
   
   # Run migrations
   npm run prisma:migrate
   ```

5. **Start the backend:**
   ```bash
   npm run start:dev
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd app/domain/admin/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```

## 📁 Project Structure

```
app/domain/admin/
├── backend/                 # NestJS Backend
│   ├── src/
│   │   ├── modules/         # Feature modules
│   │   │   ├── auth/        # Authentication
│   │   │   ├── user/        # User management
│   │   │   ├── rbac/        # Role-based access control
│   │   │   ├── form-builder/ # Dynamic form creation
│   │   │   ├── schema/      # Database schema management
│   │   │   ├── data/        # Generic CRUD operations
│   │   │   ├── audit/       # Audit logging
│   │   │   └── admin-explore/ # Admin interface
│   │   ├── common/          # Shared utilities
│   │   └── config/          # Configuration
│   ├── prisma/              # Database schema
│   └── package.json
├── frontend/                # Next.js Frontend
│   ├── src/
│   │   ├── app/             # Next.js app directory
│   │   ├── components/      # Reusable components
│   │   ├── lib/             # Utilities and API clients
│   │   └── types/           # TypeScript types
│   └── package.json
└── README.md
```

## 🔧 Key Features

### 1. Dynamic Form Builder
- Visual form designer
- Field types: text, number, date, boolean, enum, JSON, file, relations
- Validation rules and constraints
- Real-time preview

### 2. Automatic Database Generation
- Creates PostgreSQL tables from form definitions
- Handles migrations and schema updates
- Maintains data integrity

### 3. Role-Based Access Control
- Granular permissions system
- Resource-level access control
- User and role management

### 4. Data Management
- Generic CRUD operations
- Soft delete support
- Bulk operations
- Data export/import

### 5. Audit System
- Comprehensive activity logging
- User action tracking
- Data change history

### 6. Admin Interface
- Table exploration
- Data visualization
- System monitoring

## 🛠️ API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile

### Form Management
- `GET /forms` - List all forms
- `POST /forms` - Create new form
- `GET /forms/:id` - Get form details
- `POST /forms/:id/versions` - Create form version
- `POST /forms/:id/publish` - Publish form

### Data Operations
- `GET /data/:formKey` - List records
- `POST /data/:formKey` - Create record
- `GET /data/:formKey/:id` - Get record
- `PATCH /data/:formKey/:id` - Update record
- `DELETE /data/:formKey/:id` - Delete record

### User Management
- `GET /users` - List users
- `POST /users` - Create user
- `PATCH /users/:id` - Update user
- `DELETE /users/:id` - Delete user

## 🔒 Security Features

- JWT-based authentication
- Argon2 password hashing
- MFA support (TOTP)
- Role-based authorization
- Input validation and sanitization
- CORS configuration
- Rate limiting

## 📊 Database Schema

The system uses PostgreSQL with the following key tables:

- **users** - User accounts and authentication
- **roles** - Role definitions
- **permissions** - Permission definitions
- **forms** - Form metadata
- **form_versions** - Form version history
- **form_fields** - Field definitions
- **audit_logs** - Activity tracking
- **Dynamic tables** - Generated from forms

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Build and start the backend
5. Build and start the frontend

## 🧪 Testing

### Backend Tests
```bash
cd backend
npm run test
npm run test:e2e
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📝 Development

### Adding New Field Types
1. Update the `FieldType` enum in Prisma schema
2. Add validation logic in the schema service
3. Update the frontend form builder
4. Add migration logic for existing data

### Adding New Permissions
1. Update the `Permission` model
2. Add permission checks in controllers
3. Update the frontend permission system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/api/docs`

---

**Note**: This is a production-ready system with comprehensive features for dynamic form management, user administration, and data operations. The architecture supports scalability and maintainability for enterprise use.


