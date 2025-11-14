# Postman API Testing Collection

This directory contains a comprehensive Postman collection for testing the Ornakala Backend API.

## Files Included

- `Ornakala_Backend_API.postman_collection.json` - Main collection with all API endpoints
- `Ornakala_Backend_Environment.postman_environment.json` - Environment variables for the collection

## Quick Setup

1. **Import Collection**:
   - Open Postman
   - Click "Import"
   - Select `Ornakala_Backend_API.postman_collection.json`
   - Import the collection

2. **Import Environment**:
   - Click "Import" again
   - Select `Ornakala_Backend_Environment.postman_environment.json`
   - Import the environment

3. **Select Environment**:
   - In the top-right corner, select "Ornakala Backend Environment"

## API Endpoints Included

### 🩺 Health & Info
- **Health Check** - `GET /health`
- **API Info** - `GET /`

### 🔐 Authentication
- **User Signup** - `POST /auth/signup`
- **User Login** - `POST /auth/login`
- **Refresh Token** - `POST /auth/refresh`
- **User Logout** - `POST /auth/logout`

### 👤 User Management
- **Get User Profile** - `GET /auth/profile`

### 🔑 Password Management
- **Request Password Reset** - `POST /auth/request-password-reset`
- **Reset Password** - `POST /auth/reset-password`

### 🧪 Test Scenarios
- **Complete User Journey** - Multi-step test scenario

## How to Use

### Basic Testing Flow:

1. **Start with Health Check**:
   - Run "Health & Info" → "Health Check"
   - Should return `{"status": "healthy"}`

2. **Create a User Account**:
   - Run "Authentication" → "User Signup"
   - Uses predefined test credentials
   - Automatically saves tokens to environment

3. **Test Authentication**:
   - Run "Authentication" → "User Login"
   - Refreshes tokens automatically

4. **Access Protected Endpoints**:
   - Run "User Management" → "Get User Profile"
   - Uses saved access token automatically

### Environment Variables

The collection uses these variables (automatically managed):

- `base_url`: `http://3.143.178.63:8000`
- `access_token`: Set automatically after login/signup
- `refresh_token`: Set automatically after login/signup
- `test_email`: `test@ornakala.com`
- `test_password`: `SecurePass123!`

### Authentication Flow

The collection handles authentication automatically:

1. **Signup/Login** requests save tokens to environment variables
2. **Protected endpoints** use `{{access_token}}` in Authorization header
3. **Token refresh** updates the access token automatically

### Pre-Request & Test Scripts

Each request includes:

- **Pre-request scripts**: Set up base URL and authentication
- **Test scripts**: Validate responses and extract tokens
- **Response time checks**: Ensure API performance
- **Error logging**: Help debug issues

## Test Scenarios

### Complete User Journey

Run the "Test Scenarios" → "Complete User Journey" folder to test:

1. Health check ✅
2. User signup ✅
3. Profile access ✅
4. User logout ✅

Each step includes automated tests to verify success.

## Custom Testing

### Creating New Users

To test with different users, modify the request body in signup:

```json
{
    "email": "your-email@example.com",
    "password": "YourPassword123!",
    "full_name": "Your Full Name"
}
```

### Testing Error Scenarios

Try these scenarios to test error handling:

1. **Invalid credentials** in login
2. **Missing fields** in signup
3. **Expired tokens** for protected endpoints
4. **Invalid email format** in signup

## Environment Configuration

### For Different Environments:

**Local Development**:
```json
"base_url": "http://localhost:8000"
```

**Production**:
```json
"base_url": "https://your-production-domain.com"
```

### Security Notes

- Tokens are stored as **secret** variables in Postman
- Never commit real production credentials to version control
- Use different test accounts for different environments

## Troubleshooting

### Common Issues:

1. **"Request timeout" or "Server not responding"**:
   - **Domain DNS issues**: Try using the "Health Check (Direct IP)" request instead
   - **Proxy settings**: Check Postman proxy settings (Settings → Proxy)
   - **Firewall**: Ensure your firewall allows Postman network access
   - **Network**: Try switching networks or disabling VPN
   - **Alternative**: Use `{{base_url_ip}}` instead of `{{base_url}}` in requests

2. **"Unauthorized" errors**:
   - Run login again to refresh tokens
   - Check if access token is set in environment

3. **"Validation errors"**:
   - Verify request body format
   - Check required fields in API documentation

### DNS Resolution Issues:

If the domain `be-de.ornakala.com` doesn't resolve in Postman:

1. **Use Direct IP**: Switch to `{{base_url_ip}}` (http://3.143.178.63)
2. **Check DNS**: Verify domain resolves on your system: `nslookup be-de.ornakala.com`
3. **Postman Settings**: Go to Settings → General → Request timeout and increase it
4. **Proxy Settings**: Disable proxy in Postman if enabled

### Alternative Base URLs:

The environment includes both options:
- `{{base_url}}`: http://be-de.ornakala.com (primary)
- `{{base_url_ip}}`: http://3.143.178.63 (fallback)

### Network Testing:

Test connectivity outside Postman:
```bash
curl --location 'http://be-de.ornakala.com/health'
curl --location 'http://3.143.178.63/health'
```

### Getting Help

- Check the **API Documentation**: http://3.143.178.63:8000/docs
- View **OpenAPI Schema**: http://3.143.178.63:8000/openapi.json
- Review **Console logs** in Postman for detailed error messages

## Running Tests

### Manual Testing:
- Run requests individually
- Check response status and body
- Verify environment variables are set

### Automated Testing:
- Run entire collection with Collection Runner
- Use Newman CLI for CI/CD integration:
  ```bash
  newman run Ornakala_Backend_API.postman_collection.json -e Ornakala_Backend_Environment.postman_environment.json
  ```

Enjoy testing the Ornakala Backend API! 🚀