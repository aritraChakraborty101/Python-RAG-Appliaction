# Quick Start Guide

## ✅ Setup Complete!

Your Django authentication system is now running at: **http://127.0.0.1:8000/**

## 🎯 Access Points

### 🌐 Web Pages (Use Your Browser!)

1. **Home / Login Page**: http://127.0.0.1:8000/
   - Beautiful login form
   - Enter username & password
   - Auto-redirect to dashboard after login
   - Link to signup page

2. **Dashboard**: http://127.0.0.1:8000/api/auth/dashboard
   - Personalized landing page
   - View your account info
   - Test protected API endpoints
   - Interactive features (chat history, token refresh)
   - Logout button

3. **Signup Page**: http://127.0.0.1:8000/api/auth/signup-page
   - Registration form for new users
   - Real-time validation
   - Email verification

### 🔌 API Endpoints (For Programmatic Access)

4. **Signup API**: http://127.0.0.1:8000/api/auth/signup
   - POST JSON with: `username`, `email`, `password`
   - Returns 201 on success

5. **Login API**: http://127.0.0.1:8000/api/auth/login
   - POST JSON with: `username`, `password`
   - Returns JWT access and refresh tokens

6. **Token Refresh**: http://127.0.0.1:8000/api/auth/token/refresh
   - POST JSON with: `refresh` token
   - Returns new access token

### 🔒 Protected Routes (Require JWT)

7. **Chat History**: http://127.0.0.1:8000/api/auth/chat-history
   - GET with `Authorization: Bearer <token>` header
   - Example protected route

8. **Protected Test**: http://127.0.0.1:8000/api/auth/protected
   - GET with `Authorization: Bearer <token>` header
   - Another protected route for testing

### ⚙️ Admin

9. **Django Admin**: http://127.0.0.1:8000/admin
   - View registered users (create superuser first)

## 🚀 Using the System

### 🎯 Complete User Flow (Recommended)

**For Existing Users:**
1. Open browser: http://127.0.0.1:8000/
2. Login with: `testuser1` / `testpass123`
3. View your personalized dashboard
4. Test the protected features
5. Logout when done

**For New Users:**
1. Open browser: http://127.0.0.1:8000/
2. Click "Sign up here"
3. Fill registration form
4. Submit → Account created!
5. Go back to login page
6. Login with your credentials
7. Access your dashboard

### Option 1: Web Interface (Easiest)
1. Open browser to: http://127.0.0.1:8000/
2. See the login page
3. Login or signup
4. Explore the dashboard!

### Option 2: cURL Command
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "mypassword123"
  }'
```

### Option 3: Python Test Script
```bash
# Install requests first if not in venv
./venv/bin/pip install requests

# Run the test script
./venv/bin/python test_signup.py
```

## 📧 Email Configuration

**Current Status**: If you haven't configured email settings, emails won't be sent but signup will still work!

**To Enable Email Sending:**

1. Edit `.env` file:
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

2. Get Gmail App Password:
   - Go to: https://myaccount.google.com/security
   - Enable 2-Factor Authentication
   - Navigate to: Security > App passwords
   - Generate password for "Mail"
   - Copy the 16-character password to `.env`

3. Restart the server:
```bash
# Stop with Ctrl+C, then restart:
./venv/bin/python manage.py runserver
```

## 🔍 Verify Registration

### Check Database
```bash
./venv/bin/python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
User.objects.all()  # See all users
User.objects.filter(username='testuser').first()  # Find specific user
```

### Create Admin User
```bash
./venv/bin/python manage.py createsuperuser
```
Then access: http://127.0.0.1:8000/admin

## ✨ Features Demonstrated

### ✅ AUTH-001: User Registration
- POST endpoint at `/api/auth/signup`
- Validates email/username uniqueness
- Hashes passwords securely
- Returns 201 on success, 400 on error

### ✅ AUTH-002: JWT Login & Session Management
- POST `/api/auth/login` returns JWT access & refresh tokens
- Stateless authentication (no server sessions)
- Protected routes require `Authorization: Bearer <token>` header
- Token refresh endpoint for getting new access tokens
- Access tokens expire after 1 hour, refresh tokens after 7 days

### ✅ AUTH-003: Async Email Service
- Sends verification emails in background thread
- Non-blocking (API responds immediately)
- Uses real SMTP (Gmail) when configured
- Personalized email with username

## 🧪 Testing Different Scenarios

### Valid Signup
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@test.com","password":"pass123"}'
```
**Expected**: `{"message": "User registered successfully"}` (201)

### Duplicate Email
```bash
# Run the same request again
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john2","email":"john@test.com","password":"pass456"}'
```
**Expected**: `{"email": ["A user with this email already exists."]}` (400)

### Empty Password
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"jane","email":"jane@test.com","password":""}'
```
**Expected**: `{"password": ["Password cannot be empty."]}` (400)

### Login with JWT
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'
```
**Expected**: Returns access and refresh tokens (200)

### Access Protected Route
```bash
# First get token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

# Use token to access protected route
curl -X GET http://127.0.0.1:8000/api/auth/chat-history \
  -H "Authorization: Bearer $TOKEN"
```
**Expected**: Returns chat history data (200)

### Refresh Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh":"your_refresh_token_here"}'
```
**Expected**: Returns new access token (200)

### Run JWT Tests
```bash
./venv/bin/python test_jwt_auth.py
```
**Expected**: All 8 tests pass ✅

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Use different port
./venv/bin/python manage.py runserver 8001
```

### Import Errors
```bash
# Reinstall dependencies
./venv/bin/pip install -r requirements.txt
```

### Database Locked
```bash
# Delete and recreate database
rm db.sqlite3
./venv/bin/python manage.py migrate
```

## 📦 Project Files

```
.
├── authentication/
│   ├── views.py              # signup() API + signup_page() view
│   ├── serializers.py        # UserRegistrationSerializer
│   ├── emails.py             # EmailThread + send_verification_email()
│   ├── urls.py               # URL routing
│   └── templates/
│       └── authentication/
│           └── signup.html   # Beautiful signup form
├── core/
│   ├── settings.py           # SMTP config + Django settings
│   └── urls.py               # Main URL configuration
├── manage.py                 # Django management
├── requirements.txt          # Dependencies
├── test_signup.py           # Automated tests
└── .env                      # Email credentials (UPDATE THIS!)
```

## 🎉 Success!

Your authentication system is fully functional with:
- ✅ Secure password hashing
- ✅ Input validation
- ✅ Asynchronous email sending
- ✅ Beautiful web interface
- ✅ RESTful API
- ✅ JWT support ready

**Next Steps**: Configure your email credentials in `.env` to enable real email sending!
