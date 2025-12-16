# Features Documentation

Complete documentation of all features implemented in the Django RAG Chat Application.

## 🔐 Authentication System

### User Registration (AUTH-001)

**Endpoint:** `POST /api/auth/signup`

**Features:**
- Accepts username, email, and password
- Validates email and username uniqueness
- Hashes passwords using Django's `create_user()` method
- Triggers asynchronous email verification
- Non-blocking API response

**Validation Rules:**
- Username must be unique
- Email must be unique and valid format
- Password cannot be empty
- All fields are required

**Response:**
- Success: HTTP 201 with success message
- Duplicate email/username: HTTP 400 with error details

### Email Verification (AUTH-003)

**Endpoint:** `GET /api/auth/verify-email/<token>`

**Implementation:**
- Asynchronous email sending using `threading.Thread`
- SMTP configuration via Gmail
- Email credentials loaded from `.env` (secure)
- Welcome email with verification link
- Token-based verification system

**Email Template:**
- Personalized with username
- Clickable verification link
- Professional HTML styling

**Security:**
- Tokens expire after use
- One-time verification only
- Users cannot login until verified

### JWT Authentication (AUTH-002)

**Endpoints:**
- Login: `POST /api/auth/login`
- Profile: `GET /api/auth/profile`

**Features:**
- Stateless JWT token authentication
- Access and refresh tokens
- Token expiry and renewal
- Bearer token header validation

**Configuration:**
- Uses `djangorestframework-simplejwt`
- Access token lifetime: 60 minutes
- Refresh token lifetime: 1 day
- Automatic token refresh

### Web Interface

**Pages:**
- `/api/auth/signup` - User registration form
- `/api/auth/login` - Login form with JWT
- `/api/auth/profile` - User profile display
- `/api/auth/landing` - Landing page after login

**Design:**
- Bootstrap 5 Minimal White Theme
- Responsive navbar with brand and auth links
- Centered card layouts for forms
- Form-floating inputs for better UX
- Black buttons (btn-dark) on white backgrounds

## 💬 Chat System

### RAG Integration (RAG-001)

**Implementation:** `chat/rag_service.py`

**Components:**
1. **Knowledge Base:** Plain text file (`knowledge_base.txt`)
2. **Embedding Model:** SentenceTransformer (`all-MiniLM-L6-v2`)
3. **Vector Store:** FAISS index for similarity search
4. **AI Model:** Google Gemini API

**How It Works:**
1. Knowledge base is loaded and split into chunks
2. Each chunk is embedded using SentenceTransformer
3. Embeddings stored in FAISS index
4. User query is embedded and searched in FAISS
5. Top relevant chunks are retrieved
6. Context + query sent to Gemini for response

**Benefits:**
- Contextual AI responses based on your knowledge base
- Fast semantic search with FAISS
- Scalable to large knowledge bases

### Multi-Chat Support (DATA-001)

**Endpoints:**
- `POST /api/chat` - Send message (creates or continues conversation)
- `GET /api/conversations` - List all user conversations
- `GET /api/conversations/<id>` - Get conversation with messages
- `DELETE /api/conversations/<id>/delete` - Delete conversation
- `PUT /api/conversations/<id>/rename` - Rename conversation

**Features:**
- Create unlimited conversation threads
- Automatic conversation naming (based on first message)
- Manual conversation renaming
- Persistent message history
- Timestamps for all messages
- User-specific conversations (isolated per user)

**Database Models:**

**Conversation:**
- `user` - ForeignKey to User
- `title` - Conversation name
- `created_at` - Creation timestamp
- `updated_at` - Last activity timestamp

**ChatMessage:**
- `conversation` - ForeignKey to Conversation
- `user_message` - User's input
- `ai_response` - AI's reply
- `timestamp` - Message timestamp

### Chat UI

**Page:** `/chat-page`

**Features:**
- Sidebar with conversation list
- Create new conversation button
- Rename/delete conversation actions
- Message display with user/AI differentiation
- Typing animation while AI responds
- Auto-scroll to latest message
- Token storage for authentication

**Design:**
- Clean white interface
- Dark sidebar with conversation list
- Message bubbles (user: right/blue, AI: left/gray)
- Responsive layout
- Loading states and animations

### Latency Measurement

**Feature:** Real-time response time tracking

**Implementation:**
- Frontend measures time from request to response
- Displayed in milliseconds under each AI message
- Visual indicator: Green (<2s), Yellow (2-5s), Red (>5s)
- Helps monitor system performance

**Display:**
```
Response Time: 1.23s ✓
```

## ⏰ Background Task Scheduler

**Implementation:** APScheduler with Django integration

### Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| Daily Housekeeping | 2:00 AM daily | Runs all cleanup tasks |
| Weekly Cleanup | Sunday 3:00 AM | Deletes old conversations |
| Stats Generation | Every 6 hours | Generates usage statistics |

### Task Definitions

**1. delete_old_conversations()**
- Removes conversations older than 30 days
- Cascades to delete associated messages
- Logs deletion count

**2. cleanup_orphaned_messages()**
- Finds messages without conversations
- Removes data integrity issues
- Prevents database bloat

**3. cleanup_inactive_users()**
- Removes unverified users after 7 days
- Prevents spam registrations
- Cleans up incomplete signups

**4. generate_statistics()**
- Counts total users, conversations, messages
- Tracks active users (last 30 days)
- Logs system health metrics

### Manual Task Execution

**Commands:**
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

**URL:** `/scheduler-admin` (requires superuser)

**Features:**
- Live system statistics display
- One-click manual task triggers
- View scheduled jobs with next run times
- Auto-refresh every 30 seconds
- Task execution feedback

**Statistics Shown:**
- Total users
- Active users (30 days)
- Total conversations
- Total messages
- Average messages per conversation
- Database size (conversations + messages)

## 🛡️ Security Features

### Password Security
- Hashed using PBKDF2 (Django default)
- Never stored in plain text
- Minimum password requirements

### Email Security
- SMTP credentials in `.env` (not in code)
- `.env` excluded from version control
- App-specific passwords (not main password)

### API Security
- JWT token authentication required
- Token expiry enforcement
- Bearer token validation
- User-specific data isolation

### Data Privacy
- Users only see their own conversations
- Email verification required to login
- Secure token generation for verification

## 📊 Performance Features

### Caching
- RAG service singleton pattern
- FAISS index loaded once in memory
- Embeddings cached for faster retrieval

### Async Operations
- Email sending in background threads
- Non-blocking signup responses
- Scheduled tasks run independently

### Database Optimization
- Indexed foreign keys
- Cascading deletes
- Efficient query patterns

## 🎨 UI/UX Features

### Responsive Design
- Mobile-friendly layouts
- Bootstrap 5 responsive grid
- Collapsible navbar on mobile

### User Feedback
- Loading states during API calls
- Success/error notifications
- Typing indicators in chat
- Response time display

### Navigation
- Persistent navbar across pages
- Context-aware navigation (logged in/out)
- Breadcrumb trails
- Back to dashboard links

### Accessibility
- Form labels and placeholders
- Error messages
- Keyboard navigation support
- Semantic HTML structure
