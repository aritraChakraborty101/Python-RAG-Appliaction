# Background Task Scheduler - Documentation

## Overview

This application uses **APScheduler** (Advanced Python Scheduler) to run periodic background tasks for database housekeeping and maintenance. The scheduler runs automatically when the Django server starts.

## Features

### Automated Housekeeping Tasks

1. **Delete Old Conversations** (30+ days)
   - Automatically removes conversations older than 30 days
   - Cascading delete removes all associated messages
   - Helps maintain database size

2. **Cleanup Orphaned Messages**
   - Removes ChatMessages not associated with a Conversation
   - Maintains data integrity

3. **Remove Inactive Users** (7+ days)
   - Deletes users who never verified their email
   - Keeps user database clean

4. **Generate System Statistics**
   - Tracks active users, conversations, and messages
   - Monitors recent activity (last 24 hours)
   - Logs statistics for monitoring

## Schedule Configuration

### Default Schedules

| Task | Schedule | Description |
|------|----------|-------------|
| **Daily Housekeeping** | Every day at 2:00 AM | Runs all housekeeping tasks |
| **Weekly Cleanup** | Sunday at 3:00 AM | Deletes old conversations |
| **Statistics Generation** | Every 6 hours | Generates usage statistics |

### Schedule Format

The scheduler uses **Cron triggers** for time-based scheduling:

```python
# Daily at 2:00 AM
CronTrigger(hour=2, minute=0)

# Weekly on Sunday at 3:00 AM
CronTrigger(day_of_week='sun', hour=3, minute=0)

# Every 6 hours
IntervalTrigger(hours=6)
```

## Files Structure

```
chat/
├── tasks.py              # Task definitions
├── scheduler.py          # APScheduler configuration
├── apps.py              # Auto-start scheduler on Django startup
├── management/
│   └── commands/
│       ├── run_housekeeping.py    # Manual task execution
│       └── scheduler_info.py      # View scheduler status
└── templates/
    └── chat/
        └── scheduler_admin.html   # Admin web interface
```

## Usage

### 1. Automatic Startup

The scheduler starts automatically when you run the Django server:

```bash
python manage.py runserver
```

**Console Output:**
```
Initializing APScheduler...
Scheduled: Daily housekeeping at 2:00 AM
Scheduled: Weekly cleanup on Sunday at 3:00 AM
Scheduled: Statistics generation every 6 hours
APScheduler started successfully
Chat app scheduler initialized
```

### 2. Manual Task Execution

Run housekeeping tasks manually using Django management commands:

**Run All Tasks:**
```bash
python manage.py run_housekeeping
```

**Run Specific Task:**
```bash
# Delete old conversations only
python manage.py run_housekeeping --task conversations

# Cleanup orphaned messages only
python manage.py run_housekeeping --task messages

# Remove inactive users only
python manage.py run_housekeeping --task users

# Generate statistics only
python manage.py run_housekeeping --task stats
```

### 3. View Scheduler Status

Check scheduler status and scheduled jobs:

```bash
python manage.py scheduler_info
```

**Sample Output:**
```
================================================================================
APScheduler Status
================================================================================
Scheduler State: 1
Current Time: 2025-12-16 04:00:00+00:00

Total Scheduled Jobs: 3
================================================================================

Job #1:
  ID: daily_housekeeping
  Name: Daily Housekeeping Tasks
  Next Run: 2025-12-17 02:00:00+00:00
  Trigger: cron[hour='2', minute='0']

Job #2:
  ID: weekly_cleanup
  Name: Weekly Conversation Cleanup
  Next Run: 2025-12-22 03:00:00+00:00
  Trigger: cron[day_of_week='sun', hour='3', minute='0']

Job #3:
  ID: statistics_generation
  Name: Generate System Statistics
  Next Run: 2025-12-16 10:00:00+00:00
  Trigger: interval[0:06:00:00]
================================================================================
```

## Admin Web Interface

### Access the Dashboard

**URL:** http://127.0.0.1:8000/scheduler-admin

**Requirements:** Admin privileges (superuser account)

### Features

1. **Live Statistics Dashboard**
   - Active users count
   - Total conversations
   - Total messages
   - Recent activity (24h)

2. **Manual Task Triggers**
   - Run any task with one click
   - Real-time feedback
   - Auto-refresh statistics

3. **Scheduler Monitoring**
   - View scheduler status
   - List all scheduled jobs
   - Next run times
   - Job triggers

4. **Auto-Refresh**
   - Dashboard updates every 30 seconds
   - Always shows current status

## API Endpoints (Admin Only)

### Get Scheduler Status

```http
GET /api/admin/scheduler/status
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "status": "running",
  "total_jobs": 3,
  "jobs": [
    {
      "id": "daily_housekeeping",
      "name": "Daily Housekeeping Tasks",
      "next_run_time": "2025-12-17T02:00:00+00:00",
      "trigger": "cron[hour='2', minute='0']"
    }
  ]
}
```

### Trigger Manual Task

```http
POST /api/admin/scheduler/trigger
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "task": "all"
}
```

**Task Options:**
- `all` - Run all housekeeping tasks
- `conversations` - Delete old conversations
- `messages` - Cleanup orphaned messages
- `users` - Remove inactive users
- `stats` - Generate statistics

**Response:**
```json
{
  "message": "All housekeeping tasks completed",
  "result": {
    "deleted_conversations": 5,
    "cleaned_messages": 2,
    "deleted_users": 1,
    "stats": {
      "total_users": 42,
      "total_conversations": 156,
      "total_messages": 892,
      "recent_conversations_24h": 12,
      "recent_messages_24h": 34
    }
  }
}
```

### Get System Statistics

```http
GET /api/admin/scheduler/statistics
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "total_users": 42,
  "total_conversations": 156,
  "total_messages": 892,
  "recent_conversations_24h": 12,
  "recent_messages_24h": 34
}
```

## Task Definitions

### 1. delete_old_conversations()

**Purpose:** Remove conversations older than 30 days

**Logic:**
```python
cutoff_date = timezone.now() - timedelta(days=30)
old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
old_conversations.delete()
```

**Returns:** Count of deleted conversations

### 2. cleanup_orphaned_messages()

**Purpose:** Remove messages not associated with any conversation

**Logic:**
```python
orphaned = ChatMessage.objects.filter(conversation__isnull=True)
orphaned.delete()
```

**Returns:** Count of cleaned messages

### 3. cleanup_inactive_users()

**Purpose:** Remove unverified users after 7 days

**Logic:**
```python
cutoff_date = timezone.now() - timedelta(days=7)
inactive_users = User.objects.filter(
    is_active=False,
    date_joined__lt=cutoff_date
)
inactive_users.delete()
```

**Returns:** Count of deleted users

### 4. generate_statistics()

**Purpose:** Generate and log usage statistics

**Metrics:**
- Total active users
- Total conversations
- Total messages
- Recent conversations (24h)
- Recent messages (24h)

**Returns:** Dictionary of statistics

### 5. run_all_housekeeping_tasks()

**Purpose:** Master function that runs all tasks sequentially

**Returns:** Combined results from all tasks

## Customization

### Change Schedule Times

Edit `chat/scheduler.py`:

```python
# Change daily housekeeping time (current: 2:00 AM)
scheduler.add_job(
    run_all_housekeeping_tasks,
    trigger=CronTrigger(hour=2, minute=0),  # Change hour/minute here
    id='daily_housekeeping',
    name='Daily Housekeeping Tasks',
    replace_existing=True
)
```

### Change Retention Period

Edit `chat/tasks.py`:

```python
# Change conversation retention from 30 to 60 days
def delete_old_conversations():
    cutoff_date = timezone.now() - timedelta(days=60)  # Changed from 30
    old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
    old_conversations.delete()
```

### Add New Task

1. Define task function in `chat/tasks.py`:

```python
def my_custom_task():
    """My custom background task"""
    # Your logic here
    logger.info("Running custom task")
    return result
```

2. Schedule it in `chat/scheduler.py`:

```python
from .tasks import my_custom_task

scheduler.add_job(
    my_custom_task,
    trigger=IntervalTrigger(hours=12),  # Every 12 hours
    id='my_custom_task',
    name='My Custom Task',
    replace_existing=True
)
```

### Enable Test Schedule (Every 5 Minutes)

For testing purposes, uncomment these lines in `chat/scheduler.py`:

```python
scheduler.add_job(
    run_all_housekeeping_tasks,
    trigger=IntervalTrigger(minutes=5),
    id='test_housekeeping',
    name='Test Housekeeping (Every 5 min)',
    replace_existing=True
)
```

## Logging

### View Logs

All scheduler activities are logged. Check Django logs for output:

```
[INFO] Initializing APScheduler...
[INFO] Scheduled: Daily housekeeping at 2:00 AM
[INFO] APScheduler started successfully
[INFO] Starting scheduled housekeeping tasks
[INFO] Deleting 5 conversations older than 30 days
[INFO] Successfully deleted 5 old conversations
[INFO] Housekeeping tasks completed
```

### Configure Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'scheduler.log',
        },
    },
    'loggers': {
        'chat.scheduler': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'chat.tasks': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Troubleshooting

### Scheduler Not Starting

**Problem:** No scheduler logs on server start

**Solution:**
1. Check if running with `runserver` or `gunicorn`
2. Scheduler only starts in main process, not during migrations
3. Verify `chat` app is in `INSTALLED_APPS`

### Tasks Not Running

**Problem:** Scheduled time passed but task didn't run

**Solution:**
1. Verify scheduler is running: `python manage.py scheduler_info`
2. Check server is running continuously
3. Review logs for errors
4. Test manually: `python manage.py run_housekeeping`

### Permission Errors in API

**Problem:** 403 Forbidden when accessing admin endpoints

**Solution:**
1. Ensure user is superuser/admin
2. Create superuser: `python manage.py createsuperuser`
3. Use admin JWT token in Authorization header

## Production Considerations

### 1. Use Production Server

For production, use **Gunicorn** or **uWSGI** instead of Django dev server:

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### 2. Separate Worker Process

For high-traffic apps, consider using **Celery** instead of APScheduler:
- More robust for distributed systems
- Better error handling
- Separate worker processes

### 3. Database Backups

Always backup database before running destructive tasks:

```bash
# Backup before housekeeping
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Run housekeeping
python manage.py run_housekeeping
```

### 4. Monitor Task Execution

Set up monitoring for:
- Task success/failure rates
- Execution times
- Database size trends
- User activity patterns

### 5. Timezone Configuration

Ensure timezone is set correctly in `settings.py`:

```python
TIME_ZONE = 'America/New_York'  # Your timezone
USE_TZ = True
```

## Dependencies

**Required Package:**
```
apscheduler>=3.10.0
```

**Install:**
```bash
pip install apscheduler
```

## Security

### Admin-Only Access

All scheduler management endpoints require admin privileges:

```python
@permission_classes([IsAdminUser])
def scheduler_status(request):
    # Only accessible to superusers
    pass
```

### API Protection

JWT authentication required for all API endpoints:

```python
@permission_classes([IsAuthenticated])
def chat(request):
    # Requires valid JWT token
    pass
```

## Summary

✅ **Automatic** - Starts with Django server  
✅ **Configurable** - Easy to customize schedules  
✅ **Monitored** - Web dashboard and CLI tools  
✅ **Secure** - Admin-only access  
✅ **Logged** - All activities tracked  
✅ **Tested** - Manual execution available  

The scheduler helps maintain database health by automatically cleaning old data and monitoring system usage.
