# Setup & Installation Guide

This guide will help you set up and run the Django RAG Chat Application from scratch.

## Prerequisites

- Python 3.8+
- Virtual environment (venv)
- Gmail account (for SMTP email service)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Python-RAG-Appliaction
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages include:**
- Django 4.2+
- djangorestframework
- djangorestframework-simplejwt
- python-dotenv
- sentence-transformers
- faiss-cpu
- google-generativeai
- apscheduler
- numpy

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

```env
# Django Secret Key
SECRET_KEY=your-secret-key-here

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google Gemini API (for RAG)
GEMINI_API_KEY=your-gemini-api-key
```

#### Getting Gmail App Password:

1. Enable 2-Factor Authentication on your Google Account
2. Go to: https://myaccount.google.com/security
3. Navigate to "Security" > "2-Step Verification" > "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password to `.env`

#### Getting Gemini API Key:

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy it to `.env`

### 5. Run Database Migrations

```bash
python manage.py migrate
```

This creates the database schema for:
- User authentication
- Chat conversations
- Chat messages
- Email verification tokens

### 6. Create Superuser (Optional but Recommended)

```bash
python manage.py createsuperuser
```

This allows access to:
- Django admin panel: http://localhost:8000/admin
- Scheduler admin dashboard: http://localhost:8000/scheduler-admin

### 7. Prepare Knowledge Base

The RAG system uses `knowledge_base.txt` for AI responses. Edit this file to add your domain-specific knowledge.

```bash
nano knowledge_base.txt
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000**

## Verify Installation

### Test 1: Home Page
Visit: http://127.0.0.1:8000

### Test 2: Signup
1. Go to: http://127.0.0.1:8000/api/auth/signup
2. Create a test account
3. Check your email for verification link

### Test 3: Login
1. Click verification link in email
2. Go to: http://127.0.0.1:8000/api/auth/login
3. Login with credentials

### Test 4: Chat
1. Click "Django RAG Chat" in navbar
2. Create a new conversation
3. Send a test message

### Test 5: Scheduler (Admin only)
1. Create superuser if not done
2. Login as admin
3. Visit: http://127.0.0.1:8000/scheduler-admin

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Make sure virtual environment is activated and all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Email not sending

**Solution:** 
1. Check `.env` has correct Gmail credentials
2. Verify App Password (not regular password)
3. Check terminal logs for SMTP errors

### Issue: RAG responses are generic

**Solution:** 
1. Add content to `knowledge_base.txt`
2. Restart server to reload knowledge base

### Issue: Scheduler not running tasks

**Solution:** 
1. Check if scheduler is enabled in settings
2. Visit admin dashboard to verify jobs
3. Check terminal logs for errors

## Production Deployment

For production deployment, additional steps are required:

1. **Set DEBUG=False** in settings.py
2. **Use environment variables** for all secrets
3. **Configure ALLOWED_HOSTS** properly
4. **Use production-grade database** (PostgreSQL)
5. **Set up static file serving** (WhiteNoise or CDN)
6. **Use production WSGI server** (Gunicorn, uWSGI)
7. **Enable HTTPS** (Let's Encrypt)
8. **Configure CORS** for frontend if separate

## Next Steps

- Read [FEATURES.md](FEATURES.md) for detailed feature documentation
- Read [API.md](API.md) for API endpoint reference
- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
