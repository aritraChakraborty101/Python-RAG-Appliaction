# Django Authentication System with JWT and SMTP

This project implements a secure authentication system using Django REST Framework with JWT tokens and asynchronous SMTP email verification.

## Features

- **User Registration (AUTH-001)**: Secure signup endpoint with validation
- **Asynchronous Email Service (AUTH-003)**: Non-blocking email sending using threading
- **JWT Authentication**: Token-based authentication for secure API access
- **SMTP Integration**: Real email service integration (Gmail)

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

### User Registration

**Endpoint:** `POST /api/auth/signup`

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Success Response (201 Created):**
```json
{
    "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
    "email": ["A user with this email already exists."],
    "username": ["A user with this username already exists."]
}
```

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
│   ├── __init__.py
│   ├── settings.py      # Django settings with SMTP config
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── authentication/
│   ├── __init__.py
│   ├── views.py         # Signup endpoint
│   ├── serializers.py   # User registration serializer
│   ├── emails.py        # Asynchronous email service
│   └── urls.py          # Authentication routes
├── manage.py
├── requirements.txt
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── .gitignore
└── README.md
```
