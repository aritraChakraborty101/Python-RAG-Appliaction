# AUTH-002: JWT Login & Session Management

## ✅ Implementation Complete

### Overview
Implemented stateless JWT authentication using `djangorestframework-simplejwt` to replace default session-based authentication. Users can login with credentials and receive JWT tokens for accessing protected routes.

---

## 🎯 Technical Requirements Met

### ✅ Library Configuration
- **Library**: `djangorestframework-simplejwt` (already installed)
- **INSTALLED_APPS**: Added `rest_framework_simplejwt`
- **Authentication**: Configured `JWTAuthentication` as default

### ✅ Endpoints Implemented

#### 1. **POST /api/auth/login**
Login endpoint that validates credentials and returns JWT tokens.

**Request:**
```json
{
  "username": "testuser1",
  "password": "testpass123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser1",
    "email": "test1@example.com"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

#### 2. **POST /api/auth/token/refresh**
Token refresh endpoint to get new access token using refresh token.

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3. **GET /api/auth/chat-history** (Protected)
Example protected route requiring JWT authentication.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
{
  "user": "testuser1",
  "chat_history": [
    {"id": 1, "message": "Hello!", "timestamp": "2024-01-01T10:00:00Z"},
    {"id": 2, "message": "How are you?", "timestamp": "2024-01-01T10:01:00Z"}
  ]
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 4. **GET /api/auth/protected** (Protected)
Additional protected route for testing JWT authentication.

---

## ⚙️ Configuration Details

### JWT Settings (`core/settings.py`)

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # Access token valid for 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Refresh token valid for 7 days
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

---

## 🧪 Acceptance Criteria Verification

### ✅ Valid Credentials → 200 OK with JWT Tokens
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"testpass123"}'
```
**Result**: Returns 200 with `access` and `refresh` tokens ✅

### ✅ Invalid Credentials → 401 Unauthorized
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"wronguser","password":"wrongpass"}'
```
**Result**: Returns 401 with error message ✅

### ✅ Protected Routes Reject Missing Bearer Token
```bash
curl -X GET http://127.0.0.1:8000/api/auth/chat-history
```
**Result**: Returns 401 "Authentication credentials were not provided" ✅

### ✅ Protected Routes Accept Valid Bearer Token
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"testpass123"}' | jq -r .access)

curl -X GET http://127.0.0.1:8000/api/auth/chat-history \
  -H "Authorization: Bearer $TOKEN"
```
**Result**: Returns 200 with protected data ✅

---

## 📁 Files Modified

### 1. `core/settings.py`
- Added `rest_framework_simplejwt` to `INSTALLED_APPS`
- Configured `SIMPLE_JWT` settings
- Set `JWTAuthentication` as default authentication class

### 2. `authentication/views.py`
- Added `login()` view for JWT token generation
- Added `chat_history()` protected route example
- Added `protected_test()` another protected route
- Imported `RefreshToken` from `rest_framework_simplejwt.tokens`
- Imported `IsAuthenticated` permission class

### 3. `authentication/urls.py`
- Added `POST /login` endpoint
- Added `POST /token/refresh` endpoint (using built-in `TokenRefreshView`)
- Added `GET /chat-history` protected endpoint
- Added `GET /protected` protected endpoint

---

## 🔐 Security Features

1. **Stateless Authentication**: No server-side session storage
2. **Token Expiration**: Access tokens expire after 1 hour
3. **Refresh Tokens**: Long-lived tokens (7 days) for getting new access tokens
4. **HS256 Algorithm**: Secure token signing with SECRET_KEY
5. **Bearer Token Format**: Industry standard `Authorization: Bearer <token>`
6. **Password Validation**: Uses Django's authenticate() for secure credential checking

---

## 🔄 Token Workflow

1. **Registration**: User signs up via `/api/auth/signup`
2. **Login**: User logs in via `/api/auth/login` → Receives access & refresh tokens
3. **Access Protected Routes**: Include `Authorization: Bearer <access_token>` header
4. **Token Expires**: Access token expires after 1 hour
5. **Refresh Token**: Use `/api/auth/token/refresh` with refresh token → Get new access token
6. **Repeat**: Continue using new access token

---

## 🧪 Testing

### Automated Tests
Run comprehensive JWT authentication tests:
```bash
./venv/bin/python test_jwt_auth.py
```

Tests include:
- ✅ Valid login returns tokens
- ✅ Invalid login returns 401
- ✅ Missing credentials returns 400
- ✅ Protected routes reject unauthenticated requests
- ✅ Protected routes accept valid tokens
- ✅ Protected routes reject invalid tokens
- ✅ Token refresh works correctly
- ✅ Refreshed tokens work in protected routes

### Manual Testing

#### Login and Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"testpass123"}'
```

#### Access Protected Route
```bash
# Save token to variable
TOKEN="your_access_token_here"

# Use token to access protected route
curl -X GET http://127.0.0.1:8000/api/auth/chat-history \
  -H "Authorization: Bearer $TOKEN"
```

#### Refresh Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh":"your_refresh_token_here"}'
```

---

## 📊 Implementation Summary

| Requirement | Status | Notes |
|------------|--------|-------|
| djangorestframework-simplejwt installed | ✅ | Already in requirements.txt |
| Added to INSTALLED_APPS | ✅ | `rest_framework_simplejwt` |
| JWT as default authentication | ✅ | `JWTAuthentication` configured |
| POST /login endpoint | ✅ | Returns access & refresh tokens |
| Valid credentials → 200 + tokens | ✅ | Tested and verified |
| Invalid credentials → 401 | ✅ | Tested and verified |
| Protected routes require Bearer token | ✅ | Tested with /chat-history |
| Token refresh endpoint | ✅ | POST /token/refresh |
| Stateless authentication | ✅ | No session storage |

---

## 🎉 Result

All acceptance criteria for AUTH-002 have been successfully met:
- ✅ Valid login returns 200 with JWT tokens
- ✅ Invalid login returns 401
- ✅ Protected routes reject requests without Bearer token
- ✅ JWT authentication is stateless and secure
- ✅ Token refresh mechanism implemented
- ✅ Comprehensive tests pass successfully

The system now provides a complete, secure, stateless JWT authentication mechanism for API communication.
