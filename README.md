# Django RAG Chat Application

A complete full-stack AI chatbot application with secure authentication, RAG (Retrieval-Augmented Generation), multi-chat support, and automated background tasks.

## Features

### 🔐 Authentication & Security
- **User Registration**: Secure signup with email validation
- **JWT Authentication**: Token-based secure API access
- **Email Verification**: Asynchronous SMTP email service
- **Password Security**: Hashed using Django's built-in methods

### 💬 Chat System
- **RAG Integration**: AI responses powered by Google Gemini
- **FAISS Vector Search**: Semantic search over knowledge base
- **Multi-Chat Support**: Create unlimited conversation threads
- **Chat History**: Persistent storage with timestamps
- **Delete Conversations**: Clean up old chats

### ⏰ Background Task Scheduler
- **Automated Cleanup**: Removes old conversations (30+ days)
- **Data Integrity**: Cleans orphaned messages
- **User Management**: Removes inactive unverified users
- **System Monitoring**: Generates usage statistics
- **Admin Dashboard**: Web interface for task management

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Your Gmail App Password (not regular password)

**To generate Gmail App Password:**
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Go to Security > App passwords
4. Generate a new app password for "Mail"

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - JWT token login
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/verify-email/<token>` - Verify email address

### Chat
- `POST /api/chat` - Send message (create or continue conversation)
- `GET /api/chat-history` - Get chat history (legacy)
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/<id>` - Get conversation details
- `DELETE /api/conversations/<id>/delete` - Delete conversation
- `PUT /api/conversations/<id>/rename` - Rename conversation

### Scheduler (Admin Only)
- `GET /api/admin/scheduler/status` - Get scheduler status
- `POST /api/admin/scheduler/trigger` - Manually trigger tasks
- `GET /api/admin/scheduler/statistics` - Get system statistics

### Web Pages
- `/` - Home/Landing page
- `/api/auth/login` - Login page
- `/api/auth/signup` - Signup page
- `/api/auth/profile` - User profile page
- `/chat-page` - Multi-chat interface
- `/scheduler-admin` - Scheduler admin dashboard

## Technical Implementation

### AUTH-001: User Registration Logic

- **File**: `authentication/views.py`, `authentication/serializers.py`
- **Validation**: Checks for unique email/username and non-empty password
- **Security**: Passwords hashed using Django's `create_user` method
- **Integration**: Calls asynchronous email service without blocking response

### AUTH-003: Asynchronous SMTP Email Service

- **File**: `authentication/emails.py`
- **Implementation**: Uses `threading.Thread` to send emails in background
- **Configuration**: SMTP settings loaded from `.env` via `python-dotenv`
- **Security**: Credentials stored in environment variables, not in code

## Security Features

- Passwords hashed using Django's built-in password hasher (PBKDF2)
- SMTP credentials stored in `.env` file (excluded from version control)
- Email and username uniqueness validation
- Non-empty password validation
- JWT token support for future authentication endpoints

## Testing the Signup Endpoint

Using curl:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

Using HTTPie:
```bash
http POST localhost:8000/api/auth/signup username=testuser email=test@example.com password=testpass123
```

## Project Structure

```
├── core/
│   ├── settings.py           # Django settings
│   └── urls.py               # Main URL configuration
├── authentication/
│   ├── views.py              # Auth endpoints
│   ├── serializers.py        # User serializers
│   ├── emails.py             # Async email service
│   └── templates/            # Auth HTML pages
├── chat/
│   ├── models.py             # Conversation & ChatMessage models
│   ├── views.py              # Chat endpoints
│   ├── serializers.py        # Chat serializers
│   ├── rag_service.py        # RAG + FAISS integration
│   ├── tasks.py              # Background task definitions
│   ├── scheduler.py          # APScheduler configuration
│   ├── management/
│   │   └── commands/
│   │       ├── run_housekeeping.py   # Manual task execution
│   │       └── scheduler_info.py     # View scheduler status
│   └── templates/
│       └── chat/
│           ├── chat_multi.html       # Multi-chat interface
│           └── scheduler_admin.html  # Admin dashboard
├── manage.py
├── requirements.txt
├── knowledge_base.txt        # RAG knowledge base
├── .env                      # Environment variables
└── Documentation/
    ├── QUICKSTART.md         # Quick start guide
    ├── QUICKSTART-RAG.md     # RAG setup guide
    ├── QUICKSTART-SCHEDULER.md    # Scheduler quick start
    └── SCHEDULER-TASKS.md    # Detailed scheduler docs
```

## Quick Start Guides

- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup guide
- **[QUICKSTART-RAG.md](QUICKSTART-RAG.md)** - RAG & AI setup
- **[QUICKSTART-SCHEDULER.md](QUICKSTART-SCHEDULER.md)** - Scheduler quick start
- **[SCHEDULER-TASKS.md](SCHEDULER-TASKS.md)** - Detailed scheduler documentation

## Background Task Scheduler

The application includes an automated task scheduler using **APScheduler** that handles:

### Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| Daily Housekeeping | 2:00 AM daily | Runs all cleanup tasks |
| Weekly Cleanup | Sunday 3:00 AM | Deletes conversations older than 30 days |
| Statistics Generation | Every 6 hours | Generates system usage statistics |

### Manual Task Management

```bash
# View scheduler status
python manage.py scheduler_info

# Run all housekeeping tasks
python manage.py run_housekeeping

# Run specific task
python manage.py run_housekeeping --task conversations
python manage.py run_housekeeping --task messages
python manage.py run_housekeeping --task users
python manage.py run_housekeeping --task stats
```

### Admin Dashboard

Access the web dashboard at: **http://127.0.0.1:8000/scheduler-admin**

Features:
- 📊 Live system statistics
- ⚡ One-click task triggers
- 📅 View scheduled jobs
- 🔄 Auto-refresh every 30 seconds

**Requirements**: Admin/superuser account

### Task Definitions

1. **delete_old_conversations()** - Removes conversations older than 30 days
2. **cleanup_orphaned_messages()** - Removes messages not associated with conversations
3. **cleanup_inactive_users()** - Removes unverified users after 7 days
4. **generate_statistics()** - Tracks users, conversations, messages, and activity
