# API Reference

Complete API documentation for all endpoints in the Django RAG Chat Application.

## Base URL

```
http://127.0.0.1:8000
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### 1. User Signup

**Endpoint:** `POST /api/auth/signup`

**Description:** Register a new user account

**Authentication:** Not required

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
  "message": "User registered successfully. Please check your email to verify your account."
}
```

**Error Response (400 Bad Request):**
```json
{
  "username": ["A user with that username already exists."],
  "email": ["This email is already registered."]
}
```

**Notes:**
- Sends verification email asynchronously
- User cannot login until email is verified
- Password is hashed before storage

---

### 2. User Login

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and get JWT tokens

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Email not verified. Please check your email."
}
```

---

### 3. Get User Profile

**Endpoint:** `GET /api/auth/profile`

**Description:** Get authenticated user's profile information

**Authentication:** Required (JWT)

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_verified": true
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Email Verification

**Endpoint:** `GET /api/auth/verify-email/<token>`

**Description:** Verify user's email address

**Authentication:** Not required

**URL Parameters:**
- `token` (string) - Verification token from email

**Success Response (200 OK):**
```json
{
  "message": "Email verified successfully. You can now log in."
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid or expired verification token."
}
```

---

## Chat Endpoints

### 5. Send Message

**Endpoint:** `POST /api/chat`

**Description:** Send a message and get AI response

**Authentication:** Required (JWT)

**Request Body:**
```json
{
  "message": "What is Django?",
  "conversation_id": 5  // Optional: omit to create new conversation
}
```

**Success Response (200 OK):**
```json
{
  "response": "Django is a high-level Python web framework...",
  "conversation_id": 5,
  "conversation_title": "Django Question",
  "latency_ms": 1234
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Message is required"
}
```

**Notes:**
- If `conversation_id` is provided, message is added to existing conversation
- If omitted, a new conversation is created
- Conversation title is auto-generated from first message

---

### 6. List Conversations

**Endpoint:** `GET /api/conversations`

**Description:** Get all conversations for authenticated user

**Authentication:** Required (JWT)

**Success Response (200 OK):**
```json
[
  {
    "id": 5,
    "title": "Django Question",
    "created_at": "2025-12-16T10:30:00Z",
    "updated_at": "2025-12-16T10:35:00Z",
    "message_count": 3
  },
  {
    "id": 4,
    "title": "Python Tips",
    "created_at": "2025-12-15T14:20:00Z",
    "updated_at": "2025-12-15T14:25:00Z",
    "message_count": 5
  }
]
```

**Notes:**
- Sorted by most recently updated first
- Shows message count per conversation

---

### 7. Get Conversation Details

**Endpoint:** `GET /api/conversations/<id>`

**Description:** Get conversation with all messages

**Authentication:** Required (JWT)

**URL Parameters:**
- `id` (integer) - Conversation ID

**Success Response (200 OK):**
```json
{
  "id": 5,
  "title": "Django Question",
  "created_at": "2025-12-16T10:30:00Z",
  "updated_at": "2025-12-16T10:35:00Z",
  "messages": [
    {
      "id": 12,
      "user_message": "What is Django?",
      "ai_response": "Django is a high-level Python web framework...",
      "timestamp": "2025-12-16T10:30:15Z"
    },
    {
      "id": 13,
      "user_message": "How do I install it?",
      "ai_response": "You can install Django using pip...",
      "timestamp": "2025-12-16T10:32:20Z"
    }
  ]
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Conversation not found"
}
```

---

### 8. Rename Conversation

**Endpoint:** `PUT /api/conversations/<id>/rename`

**Description:** Change conversation title

**Authentication:** Required (JWT)

**URL Parameters:**
- `id` (integer) - Conversation ID

**Request Body:**
```json
{
  "title": "My Django Learning"
}
```

**Success Response (200 OK):**
```json
{
  "id": 5,
  "title": "My Django Learning",
  "updated_at": "2025-12-16T10:40:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Title is required"
}
```

---

### 9. Delete Conversation

**Endpoint:** `DELETE /api/conversations/<id>/delete`

**Description:** Delete conversation and all its messages

**Authentication:** Required (JWT)

**URL Parameters:**
- `id` (integer) - Conversation ID

**Success Response (200 OK):**
```json
{
  "message": "Conversation deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Conversation not found"
}
```

**Notes:**
- Cascading delete removes all associated messages
- Cannot be undone

---

### 10. Get Chat History (Legacy)

**Endpoint:** `GET /api/chat-history`

**Description:** Get all messages for authenticated user (legacy endpoint)

**Authentication:** Required (JWT)

**Success Response (200 OK):**
```json
[
  {
    "id": 12,
    "user_message": "What is Django?",
    "ai_response": "Django is a high-level Python web framework...",
    "timestamp": "2025-12-16T10:30:15Z"
  },
  {
    "id": 13,
    "user_message": "How do I install it?",
    "ai_response": "You can install Django using pip...",
    "timestamp": "2025-12-16T10:32:20Z"
  }
]
```

**Notes:**
- This endpoint returns all messages regardless of conversation
- Use `/api/conversations/<id>` for conversation-specific messages
- Kept for backward compatibility

---

## Scheduler Endpoints (Admin Only)

### 11. Get Scheduler Status

**Endpoint:** `GET /api/admin/scheduler/status`

**Description:** Get scheduler status and scheduled jobs

**Authentication:** Required (JWT + Superuser)

**Success Response (200 OK):**
```json
{
  "scheduler_running": true,
  "jobs": [
    {
      "id": "daily_housekeeping",
      "name": "Daily Housekeeping",
      "trigger": "cron",
      "next_run_time": "2025-12-17T02:00:00Z"
    },
    {
      "id": "weekly_cleanup",
      "name": "Weekly Cleanup",
      "trigger": "cron",
      "next_run_time": "2025-12-22T03:00:00Z"
    }
  ]
}
```

**Error Response (403 Forbidden):**
```json
{
  "error": "Admin access required"
}
```

---

### 12. Trigger Manual Task

**Endpoint:** `POST /api/admin/scheduler/trigger`

**Description:** Manually trigger a scheduled task

**Authentication:** Required (JWT + Superuser)

**Request Body:**
```json
{
  "task": "conversations"  // Options: conversations, messages, users, stats, all
}
```

**Success Response (200 OK):**
```json
{
  "message": "Task 'conversations' triggered successfully",
  "result": "Deleted 5 old conversations"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid task name"
}
```

---

### 13. Get System Statistics

**Endpoint:** `GET /api/admin/scheduler/statistics`

**Description:** Get system usage statistics

**Authentication:** Required (JWT + Superuser)

**Success Response (200 OK):**
```json
{
  "total_users": 150,
  "active_users_30d": 85,
  "total_conversations": 450,
  "total_messages": 1850,
  "avg_messages_per_conversation": 4.11,
  "generated_at": "2025-12-16T10:45:00Z"
}
```

---

## Web Pages (HTML)

### Authentication Pages
- `GET /api/auth/signup` - Signup form
- `GET /api/auth/login` - Login form
- `GET /api/auth/profile` - User profile page
- `GET /api/auth/landing` - Landing page

### Application Pages
- `GET /` - Home page (redirects based on auth status)
- `GET /chat-page` - Multi-chat interface
- `GET /scheduler-admin` - Scheduler admin dashboard (superuser only)

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Email not verified or insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:
- Django-ratelimit
- API throttling in DRF
- NGINX rate limiting

---

## Testing with cURL

### Signup
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Send Message
```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"message":"What is Django?"}'
```

### List Conversations
```bash
curl -X GET http://127.0.0.1:8000/api/conversations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
