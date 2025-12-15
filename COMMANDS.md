# Quick Commands Reference

## 🚀 Server Commands

```bash
# Start server
./venv/bin/python manage.py runserver

# Start on different port
./venv/bin/python manage.py runserver 8001

# Stop server
Press Ctrl+C
```

## 🧪 Testing Commands

### Test via cURL

```bash
# Valid signup
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@test.com","password":"pass123"}'

# Duplicate email test
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"jane","email":"john@test.com","password":"pass456"}'

# Empty password test
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@test.com","password":""}'
```

### Test via Python Script

```bash
# Run automated tests
./venv/bin/python test_signup.py
```

## 🗄️ Database Commands

```bash
# Run migrations
./venv/bin/python manage.py migrate

# Create superuser for admin panel
./venv/bin/python manage.py createsuperuser

# Open Django shell
./venv/bin/python manage.py shell

# View all users (in shell)
from django.contrib.auth.models import User
User.objects.all()

# View specific user (in shell)
User.objects.filter(username='testuser').first()

# Delete all users (in shell)
User.objects.all().delete()

# Reset database
rm db.sqlite3
./venv/bin/python manage.py migrate
```

## 📦 Dependency Commands

```bash
# Install dependencies
./venv/bin/pip install -r requirements.txt

# Add new dependency
./venv/bin/pip install package-name
./venv/bin/pip freeze > requirements.txt

# Update dependencies
./venv/bin/pip install --upgrade -r requirements.txt
```

## 🔐 Virtual Environment Commands

```bash
# Create virtual environment (already done)
python3 -m venv venv

# Activate venv (if needed manually)
source venv/bin/activate

# Deactivate venv
deactivate
```

## 🌐 Quick Access URLs

```bash
# Open web form
xdg-open http://127.0.0.1:8000/api/auth/signup-page

# Or manually visit:
http://127.0.0.1:8000/                        # Redirects to signup page
http://127.0.0.1:8000/api/auth/signup-page    # HTML signup form
http://127.0.0.1:8000/api/auth/signup         # JSON API endpoint
http://127.0.0.1:8000/admin                   # Django admin
```

## 📧 Email Configuration

```bash
# Edit environment file
nano .env

# Required variables:
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password

# Test email sending (in Django shell)
./venv/bin/python manage.py shell
>>> from authentication.emails import send_verification_email
>>> send_verification_email('testuser', 'test@example.com')
```

## 🐛 Debugging Commands

```bash
# Check for errors
./venv/bin/python manage.py check

# View recent server logs
# (they appear in the terminal where server is running)

# Enable debug mode (already enabled in .env)
# DEBUG=True in .env

# View settings
./venv/bin/python manage.py diffsettings
```

## 🧹 Cleanup Commands

```bash
# Remove cache files
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove database (careful!)
rm db.sqlite3

# Remove virtual environment (careful!)
rm -rf venv

# Start fresh
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python manage.py migrate
```

## 📊 Useful One-Liners

```bash
# Count registered users
./venv/bin/python manage.py shell -c "from django.contrib.auth.models import User; print(f'Total users: {User.objects.count()}')"

# List all usernames
./venv/bin/python manage.py shell -c "from django.contrib.auth.models import User; [print(u.username) for u in User.objects.all()]"

# Check if email exists
./venv/bin/python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(email='test@example.com').exists())"

# Test API and show response
curl -s -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass"}' | python3 -m json.tool
```

## 🎯 Common Workflows

### Fresh Start
```bash
./venv/bin/python manage.py runserver
# Visit http://127.0.0.1:8000/api/auth/signup-page
```

### Testing Cycle
```bash
# Delete database
rm db.sqlite3

# Recreate
./venv/bin/python manage.py migrate

# Run tests
./venv/bin/python test_signup.py

# Or test manually via web form
```

### Production Prep
```bash
# 1. Update .env with real credentials
# 2. Change DEBUG=False in .env
# 3. Set proper ALLOWED_HOSTS in .env
# 4. Use production WSGI server (gunicorn/uwsgi)
```

## 💡 Tips

- Press **Ctrl+C** to stop the server
- Use **Ctrl+Shift+R** in browser to hard refresh
- Check terminal where server runs for real-time logs
- Django admin requires superuser: `./venv/bin/python manage.py createsuperuser`
- Emails are sent in background thread (non-blocking)
- Configure `.env` for real email sending (optional for testing)
