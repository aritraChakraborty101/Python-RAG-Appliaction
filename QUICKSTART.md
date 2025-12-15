# Quick Start Guide

## ✅ Setup Complete!

Your Django authentication system is now running at: **http://127.0.0.1:8000/**

## 🎯 Access Points

1. **Signup Web Interface**: http://127.0.0.1:8000/api/auth/signup-page
   - Beautiful HTML form for user registration
   - Real-time validation and feedback
   - Automatic email sending on successful signup

2. **API Endpoint**: http://127.0.0.1:8000/api/auth/signup
   - Use this for programmatic access
   - POST JSON with: `username`, `email`, `password`

3. **Django Admin**: http://127.0.0.1:8000/admin
   - View registered users (create superuser first)

## 🚀 Testing the System

### Option 1: Web Interface (Easiest)
1. Open browser to: http://127.0.0.1:8000/api/auth/signup-page
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `mypassword123`
3. Click "Create Account"
4. Check for success message!

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
