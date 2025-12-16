# Django RAG Chat Application

A complete full-stack AI chatbot application with secure authentication, RAG (Retrieval-Augmented Generation), multi-chat support, and automated background tasks.

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete installation and setup guide
- **[FEATURES.md](FEATURES.md)** - Detailed feature documentation
- **[API.md](API.md)** - Complete API reference
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guidelines and technical details

## ✨ Features Overview

### 🔐 Authentication & Security
- User registration with email verification
- JWT token-based authentication
- Asynchronous SMTP email service
- Secure password hashing

### 💬 AI Chat System
- RAG-powered AI responses (Google Gemini)
- FAISS vector search for semantic retrieval
- Multi-conversation support
- Persistent chat history with timestamps
- Response latency tracking

### ⏰ Background Task Scheduler
- Automated cleanup of old conversations (30+ days)
- Data integrity maintenance
- User management (inactive/unverified cleanup)
- System statistics generation
- Web-based admin dashboard

### 🎨 User Interface
- Bootstrap 5 minimal white theme
- Responsive design
- Multi-chat interface with sidebar
- Real-time message updates
- Profile management

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Python-RAG-Appliaction
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials:
# - EMAIL_HOST_USER (Gmail)
# - EMAIL_HOST_PASSWORD (App Password)
# - GEMINI_API_KEY (Google AI)
```

### 3. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional but recommended
```

### 4. Run Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## 📖 Documentation Structure

### For Users
- **[SETUP.md](SETUP.md)** - Installation, configuration, and troubleshooting
- **[FEATURES.md](FEATURES.md)** - Feature descriptions and usage guides
- **[API.md](API.md)** - API endpoints, request/response examples

### For Developers
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Architecture, code style, deployment
- **[API.md](API.md)** - Technical API specifications
- **[FEATURES.md](FEATURES.md)** - Implementation details

## 🔧 Key Technologies

- **Backend:** Django 4.2+, Django REST Framework
- **Authentication:** JWT (djangorestframework-simplejwt)
- **AI/ML:** Google Gemini, SentenceTransformers, FAISS
- **Task Scheduling:** APScheduler
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Email:** Gmail SMTP (async with threading)

## 📊 Project Structure

```
Python-RAG-Appliaction/
├── authentication/        # User auth & email verification
├── chat/                  # Chat, RAG, and scheduler
├── core/                  # Django settings & root URLs
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
├── knowledge_base.txt     # RAG knowledge base
├── .env                   # Environment variables (not in git)
└── Documentation/
    ├── README.md          # This file
    ├── SETUP.md           # Setup guide
    ├── FEATURES.md        # Feature documentation
    ├── API.md             # API reference
    └── DEVELOPMENT.md     # Development guide
```

## 🔑 Quick Commands

```bash
# Run server
python manage.py runserver

# View scheduler status
python manage.py scheduler_info

# Run housekeeping tasks
python manage.py run_housekeeping

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

## 🌐 Web Interface

- **Home:** http://127.0.0.1:8000/
- **Signup:** http://127.0.0.1:8000/api/auth/signup
- **Login:** http://127.0.0.1:8000/api/auth/login
- **Profile:** http://127.0.0.1:8000/api/auth/profile
- **Chat:** http://127.0.0.1:8000/chat-page
- **Scheduler Admin:** http://127.0.0.1:8000/scheduler-admin (superuser)

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/verify-email/<token>` - Verify email

### Chat
- `POST /api/chat` - Send message
- `GET /api/conversations` - List conversations
- `GET /api/conversations/<id>` - Get conversation details
- `DELETE /api/conversations/<id>/delete` - Delete conversation
- `PUT /api/conversations/<id>/rename` - Rename conversation

### Admin (Scheduler)
- `GET /api/admin/scheduler/status` - Scheduler status
- `POST /api/admin/scheduler/trigger` - Trigger tasks
- `GET /api/admin/scheduler/statistics` - System stats

**See [API.md](API.md) for complete API documentation.**

## 🛡️ Security

- Passwords hashed with PBKDF2
- JWT token authentication
- Email verification required
- Environment variables for secrets
- User data isolation
- CSRF protection

## 📄 License

This project is for educational and assessment purposes.

## 🤝 Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines.
