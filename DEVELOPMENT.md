# Development Guide

Technical guidelines, architecture details, and development workflow for the Django RAG Chat Application.

---

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Database Models](#database-models)
- [Key Implementation Details](#key-implementation-details)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Security Best Practices](#security-best-practices)
- [Performance Optimization](#performance-optimization)
- [Testing Guidelines](#testing-guidelines)
- [Deployment Checklist](#deployment-checklist)
- [Useful Commands](#useful-commands)

---

## Project Structure

```
Python-RAG-Appliaction/
├── core/                          # Django project settings
│   ├── settings.py               # Main configuration
│   ├── urls.py                   # Root URL routing
│   └── wsgi.py                   # WSGI entry point
│
├── authentication/               # Auth app
│   ├── models.py                # EmailVerification model
│   ├── views.py                 # Signup, login, profile views
│   ├── serializers.py           # User serializers
│   ├── emails.py                # Async email service
│   ├── urls.py                  # Auth URL patterns
│   └── templates/
│       └── authentication/      # Auth HTML templates
│           ├── signup.html
│           ├── login.html
│           ├── profile.html
│           └── landing.html
│
├── chat/                         # Chat app
│   ├── models.py                # Conversation & ChatMessage models
│   ├── views.py                 # Chat endpoints
│   ├── serializers.py           # Chat serializers
│   ├── rag_service.py           # RAG + FAISS logic
│   ├── tasks.py                 # Scheduled task definitions
│   ├── scheduler.py             # APScheduler setup
│   ├── urls.py                  # Chat URL patterns
│   ├── management/
│   │   └── commands/
│   │       ├── run_housekeeping.py    # Manual task trigger
│   │       └── scheduler_info.py      # View scheduler status
│   └── templates/
│       └── chat/
│           ├── chat_multi.html        # Multi-chat interface
│           └── scheduler_admin.html   # Admin dashboard
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── knowledge_base.txt            # RAG knowledge base
├── .env                          # Environment variables (ignored by git)
├── .env.example                  # Environment template
├── db.sqlite3                    # SQLite database
│
└── Documentation/
    ├── README.md                 # Main documentation
    ├── SETUP.md                  # Setup guide
    ├── FEATURES.md               # Feature documentation
    ├── API.md                    # API reference
    └── DEVELOPMENT.md            # This file
```

---

## Technology Stack

### Backend Frameworks
- **Framework:** Django 4.2+
- **API:** Django REST Framework
- **Authentication:** djangorestframework-simplejwt
- **Task Scheduler:** APScheduler
- **Database:** SQLite (development), PostgreSQL (recommended for production)

### AI & ML
- **LLM:** Google Gemini API
- **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
- **Vector Store:** FAISS (Facebook AI Similarity Search)

### Frontend
- **Framework:** Bootstrap 5
- **Theme:** Minimal White Mode
- **JavaScript:** Vanilla JS (no framework)

### Email
- **Service:** Gmail SMTP
- **Implementation:** Threading-based async

---

## Database Models

### User (Django built-in)
- `username` - CharField, unique
- `email` - EmailField, unique
- `password` - CharField (hashed)
- `is_active` - BooleanField
- `date_joined` - DateTimeField

### EmailVerification
```python
class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Conversation
```python
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ChatMessage
```python
class ChatMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

## Key Implementation Details

### 1. Asynchronous Email Service

**File:** `authentication/emails.py`

```python
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    
    def run(self):
        self.email_message.send()

def send_verification_email(user, request):
    # Create token
    # Build email
    # Start thread (non-blocking)
    EmailThread(email_message).start()
```

**Benefits:**
- Non-blocking API responses
- User doesn't wait for SMTP
- Better user experience

### 2. RAG Service Architecture

**File:** `chat/rag_service.py`

**Flow:**
1. Load `knowledge_base.txt` on startup
2. Split text into chunks (~500 chars)
3. Generate embeddings with SentenceTransformer
4. Store in FAISS index
5. For each query:
   - Embed query
   - Search FAISS for top 3 similar chunks
   - Build context from retrieved chunks
   - Send to Gemini with prompt template
   - Return AI response

**Singleton Pattern:**
```python
_rag_service_instance = None

def get_rag_service():
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
```

### 3. JWT Authentication Flow

**Login:**
1. User submits username + password
2. Django authenticates credentials
3. Check email verification status
4. Generate access + refresh tokens
5. Return tokens + user info

**Protected Endpoints:**
1. Frontend sends: `Authorization: Bearer <token>`
2. Django validates token
3. Extract user from token
4. Process request with authenticated user

### 4. Task Scheduler Implementation

**File:** `chat/scheduler.py`

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# Daily at 2 AM
scheduler.add_job(daily_housekeeping, 'cron', hour=2)

# Weekly on Sunday at 3 AM
scheduler.add_job(weekly_cleanup, 'cron', day_of_week='sun', hour=3)

# Every 6 hours
scheduler.add_job(generate_statistics, 'interval', hours=6)

scheduler.start()
```

**Django Integration:**
- Scheduler starts with app (AppConfig.ready())
- Runs in background thread
- Persists across requests
- Independent of web workers

### 5. Multi-Chat Architecture

**Conversation Management:**
- Each user has multiple conversations
- Conversations have unique IDs
- Messages belong to conversations
- Cascading deletes (conversation → messages)

**Frontend State:**
- Active conversation ID stored
- Sidebar shows conversation list
- Click to switch conversations
- Auto-load messages for active conversation

---

## Development Workflow

### Adding a New Feature

1. **Create branch:**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Modify models (if needed):**
   ```python
   # In models.py
   class NewModel(models.Model):
       # fields here
   ```

3. **Create migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create serializer:**
   ```python
   # In serializers.py
   class NewModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = NewModel
           fields = '__all__'
   ```

5. **Create view:**
   ```python
   # In views.py
   @api_view(['GET', 'POST'])
   @permission_classes([IsAuthenticated])
   def new_endpoint(request):
       # logic here
   ```

6. **Add URL route:**
   ```python
   # In urls.py
   path('new-endpoint/', views.new_endpoint, name='new-endpoint'),
   ```

7. **Test:**
   ```bash
   python manage.py runserver
   # Test with curl or browser
   ```

8. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

### Testing

**Manual Testing:**
```bash
# Start server
python manage.py runserver

# Test endpoints
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'
```

**Python Shell Testing:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from chat.models import Conversation, ChatMessage

# Test data creation
user = User.objects.create_user('testuser', 'test@test.com', 'password')
conv = Conversation.objects.create(user=user, title='Test')
msg = ChatMessage.objects.create(
    conversation=conv,
    user_message='Test message',
    ai_response='Test response'
)
```

### Debugging

**Django Debug Toolbar:**
```bash
pip install django-debug-toolbar
```

**Logging:**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
```

**Check logs in terminal:**
- Watch server output while making requests
- Check for errors, warnings, SQL queries

---

## Code Style Guidelines

### Python (PEP 8)
- Use 4 spaces for indentation
- Max line length: 79 characters
- Use snake_case for variables and functions
- Use PascalCase for class names
- Add docstrings to functions and classes

### JavaScript
- Use camelCase for variables and functions
- Use const/let (not var)
- Add comments for complex logic
- Use template literals for strings

### HTML/CSS
- Use semantic HTML5 tags
- Bootstrap classes for styling
- Minimal custom CSS
- Mobile-first responsive design

---

## Security Best Practices

### 1. Environment Variables
- Never commit `.env` file
- Use `.env.example` as template
- Load with `python-dotenv`

### 2. Password Security
- Always use Django's `create_user()` or `make_password()`
- Never store plain text passwords
- Enforce password strength (custom validator)

### 3. API Security
- Require authentication for sensitive endpoints
- Validate all user input
- Use Django's CSRF protection
- Rate limiting for production

### 4. Database Security
- Use parameterized queries (Django ORM does this)
- Validate foreign keys
- User isolation (filter by request.user)

---

## Performance Optimization

### 1. Database
- Use select_related() for ForeignKey
- Use prefetch_related() for ManyToMany
- Add indexes on frequently queried fields
- Use pagination for large result sets

### 2. Caching
- Cache RAG service instance (singleton)
- Cache FAISS index in memory
- Use Django cache framework for repeated queries

### 3. Frontend
- Minimize DOM manipulations
- Use event delegation
- Lazy load conversations
- Debounce search inputs

---

## Testing Guidelines

### Manual Testing

Test all endpoints using curl or Postman:

```bash
# Test signup
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"testpass123"}'

# Test login
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Test chat (with token)
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"What is Django?"}'
```

### Python Shell Testing

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from chat.models import Conversation, ChatMessage

# Test user creation
user = User.objects.create_user('testuser', 'test@test.com', 'password123')
print(f"Created user: {user.username}")

# Test conversation creation
conv = Conversation.objects.create(user=user, title='Test Conversation')
print(f"Created conversation: {conv.title}")

# Test message creation
msg = ChatMessage.objects.create(
    conversation=conv,
    user_message='Hello AI',
    ai_response='Hello! How can I help you?'
)
print(f"Created message: {msg.id}")

# Verify data
print(f"User conversations: {user.conversation_set.count()}")
print(f"Conversation messages: {conv.chatmessage_set.count()}")
```

### Integration Testing

Test the RAG service:

```bash
python manage.py shell
```

```python
from chat.rag_service import get_rag_service

# Initialize RAG service
rag = get_rag_service()
rag.initialize()

# Test query
response = rag.get_response("What is Python?")
print(f"AI Response: {response}")
```

### Test Scheduler

```bash
# Check scheduler status
python manage.py scheduler_info

# Run manual task
python manage.py run_housekeeping --task stats

# Check if tasks are logged
tail -f nohup.out  # Or check server output
```

---

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL)
- [ ] Set up static file serving (WhiteNoise)
- [ ] Use production WSGI server (Gunicorn)
- [ ] Enable HTTPS
- [ ] Set up error logging (Sentry)
- [ ] Configure CORS properly
- [ ] Use environment variables for all secrets
- [ ] Set up database backups
- [ ] Configure email backend for production
- [ ] Set up monitoring (Uptime checks)

---

## Useful Commands

### Django Management

```bash
# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver

# Django shell
python manage.py shell

# View scheduler status
python manage.py scheduler_info

# Run housekeeping tasks
python manage.py run_housekeeping

# Collect static files
python manage.py collectstatic

# Create app
python manage.py startapp app_name

# Database shell
python manage.py dbshell
```

### Git Commands

```bash
# Check status
git status

# Create branch
git checkout -b feature/feature-name

# Commit changes
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/feature-name

# View logs
git log --oneline --graph
```

### Database Commands

```bash
# Django shell
python manage.py shell

# Database shell
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate app_name migration_number
```

---

## Troubleshooting Common Issues

### Issue: Migrations out of sync
```bash
python manage.py migrate --fake-initial
```

### Issue: Database locked
```bash
# Kill Django processes
pkill -f runserver
# Remove lock file
rm db.sqlite3-journal
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --clear
```

### Issue: RAG responses not working
- Check `knowledge_base.txt` exists
- Verify Gemini API key in `.env`
- Check terminal for errors

---

## Contributing

### Contribution Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow code style guidelines
4. **Test thoroughly**: Manual and automated tests
5. **Commit**: `git commit -m "Add amazing feature"`
6. **Push**: `git push origin feature/amazing-feature`
7. **Submit Pull Request**: Describe changes clearly
8. **Wait for review**: Address feedback if needed

### Pull Request Guidelines

- **Clear Description**: Explain what and why
- **Small Changes**: Keep PRs focused and reviewable
- **Tests**: Include tests for new features
- **Documentation**: Update docs if needed
- **Code Style**: Follow project conventions

---

## Resources

### Official Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [FAISS Documentation](https://faiss.ai/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

### AI & ML Resources
- [Google Gemini API](https://ai.google.dev/docs)
- [SentenceTransformers](https://www.sbert.net/)
- [Hugging Face Models](https://huggingface.co/models)

### Python Resources
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Documentation](https://docs.python.org/3/)
- [Virtual Environments](https://docs.python.org/3/library/venv.html)

---

**Happy Coding! 🚀**
