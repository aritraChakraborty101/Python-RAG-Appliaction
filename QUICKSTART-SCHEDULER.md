# Quick Start: Background Task Scheduler

## What Is This?

An automated background task system that keeps your database clean and monitors system health. It runs automatically in the background without any manual intervention.

## What It Does

✅ **Deletes old conversations** (30+ days old)  
✅ **Removes orphaned messages** (data cleanup)  
✅ **Cleans inactive users** (never verified email after 7 days)  
✅ **Generates statistics** (tracks usage patterns)  

All tasks run automatically on schedule - no manual work needed!

## Quick Test (5 minutes)

### Step 1: Start the Server

```bash
cd /home/aritra/Programming/spartect-assesment/Python-RAG-Appliaction
source venv/bin/activate
python manage.py runserver
```

✅ **Scheduler auto-starts** with the server!

### Step 2: Run Manual Test

Open a new terminal:

```bash
cd /home/aritra/Programming/spartect-assesment/Python-RAG-Appliaction
source venv/bin/activate
python test_scheduler.py
```

You'll see:
- Scheduler starts ✓
- 3 jobs scheduled ✓
- Statistics generated ✓

### Step 3: View Scheduled Jobs

```bash
python manage.py scheduler_info
```

Shows all scheduled jobs and their next run times.

### Step 4: Run Housekeeping Manually

```bash
# Run all tasks
python manage.py run_housekeeping

# Or run specific task
python manage.py run_housekeeping --task stats
```

### Step 5: Access Admin Dashboard

1. **Create superuser** (if you haven't):
   ```bash
   python manage.py createsuperuser
   ```

2. **Login** at: http://127.0.0.1:8000/api/auth/login

3. **Visit dashboard**: http://127.0.0.1:8000/scheduler-admin

4. **Features**:
   - Live statistics
   - Manual task triggers
   - Scheduler status
   - Job monitoring

## Default Schedule

| Task | When | What It Does |
|------|------|--------------|
| **Daily Housekeeping** | 2:00 AM | Runs all cleanup tasks |
| **Weekly Cleanup** | Sunday 3:00 AM | Deletes old conversations |
| **Statistics** | Every 6 hours | Generates usage stats |

## Manual Commands

```bash
# View scheduler status
python manage.py scheduler_info

# Run all housekeeping tasks
python manage.py run_housekeeping

# Run specific tasks
python manage.py run_housekeeping --task conversations  # Delete old
python manage.py run_housekeeping --task messages       # Cleanup orphaned
python manage.py run_housekeeping --task users          # Remove inactive
python manage.py run_housekeeping --task stats          # Generate stats
```

## API Endpoints (Admin Only)

```bash
# Get scheduler status
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://127.0.0.1:8000/api/admin/scheduler/status

# Trigger task manually
curl -X POST \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"task": "all"}' \
     http://127.0.0.1:8000/api/admin/scheduler/trigger

# Get statistics
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://127.0.0.1:8000/api/admin/scheduler/statistics
```

## Web Dashboard

**URL**: http://127.0.0.1:8000/scheduler-admin

**Features**:
- 📊 Live statistics dashboard
- ⚡ One-click task triggers
- 📅 View scheduled jobs
- 🔄 Auto-refresh every 30 seconds

**Requirements**: Admin/superuser account

## Customization

### Change Schedule Times

Edit `chat/scheduler.py`:

```python
# Change daily housekeeping time (line ~35)
scheduler.add_job(
    run_all_housekeeping_tasks,
    trigger=CronTrigger(hour=3, minute=30),  # 3:30 AM instead of 2:00 AM
    id='daily_housekeeping',
    name='Daily Housekeeping Tasks',
    replace_existing=True
)
```

### Change Retention Period

Edit `chat/tasks.py`:

```python
# Change from 30 to 60 days (line ~16)
def delete_old_conversations():
    cutoff_date = timezone.now() - timedelta(days=60)  # Changed
    old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
    ...
```

### Enable Test Mode (Every 5 Minutes)

Edit `chat/scheduler.py`, uncomment lines 61-68:

```python
scheduler.add_job(
    run_all_housekeeping_tasks,
    trigger=IntervalTrigger(minutes=5),
    id='test_housekeeping',
    name='Test Housekeeping (Every 5 min)',
    replace_existing=True
)
```

⚠️ **Remember**: Disable this in production!

## Troubleshooting

### Scheduler Not Starting?

**Check**:
1. Server running? `python manage.py runserver`
2. APScheduler installed? `pip install apscheduler`
3. Check console for errors

**Test**:
```bash
python test_scheduler.py
```

### Tasks Not Running?

**Debug**:
```bash
# View scheduled jobs
python manage.py scheduler_info

# Run manually to check for errors
python manage.py run_housekeeping

# Check logs
python manage.py runserver  # Watch console output
```

### Admin Dashboard Shows 403 Forbidden?

**Solution**:
1. Create superuser: `python manage.py createsuperuser`
2. Login as admin
3. Get admin JWT token
4. Use token in API requests

## Files Overview

```
chat/
├── tasks.py              # Task definitions (what to run)
├── scheduler.py          # Schedule config (when to run)
├── apps.py              # Auto-start on server startup
├── management/
│   └── commands/
│       ├── run_housekeeping.py     # Manual execution
│       └── scheduler_info.py       # View status
└── templates/
    └── chat/
        └── scheduler_admin.html    # Web dashboard
```

## Example Output

### Scheduler Info

```bash
$ python manage.py scheduler_info

================================================================================
APScheduler Status
================================================================================
Scheduler State: 1
Current Time: 2025-12-16 04:08:00+00:00

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
  Next Run: 2025-12-21 03:00:00+00:00
  Trigger: cron[day_of_week='sun', hour='3', minute='0']

Job #3:
  ID: statistics_generation
  Name: Generate System Statistics
  Next Run: 2025-12-16 10:08:00+00:00
  Trigger: interval[6:00:00]
================================================================================
```

### Run Housekeeping

```bash
$ python manage.py run_housekeeping

============================================================
Running Housekeeping Tasks
============================================================

Deleted: 5 conversations, 2 orphaned messages, 1 inactive users
Stats: {
  'total_users': 42,
  'total_conversations': 156,
  'total_messages': 892,
  'recent_messages_24h': 34
}
============================================================
Housekeeping completed successfully!
============================================================
```

## Key Features

✅ **Zero Configuration** - Works out of the box  
✅ **Auto-Start** - Begins with Django server  
✅ **Safe Operations** - Only deletes old/orphaned data  
✅ **Admin Control** - Web dashboard + CLI tools  
✅ **Monitored** - Logs all activities  
✅ **Customizable** - Easy to modify schedules  

## Next Steps

1. ✅ Run test: `python test_scheduler.py`
2. ✅ View dashboard: http://127.0.0.1:8000/scheduler-admin
3. ✅ Customize schedules (optional)
4. ✅ Set up production logging
5. ✅ Monitor task execution

## Production Tips

### Use Real WSGI Server

```bash
# Don't use runserver in production
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Set Up Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'scheduler.log',
        },
    },
    'loggers': {
        'chat.scheduler': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Monitor Tasks

- Set up alerts for failed tasks
- Track database size trends
- Monitor task execution times
- Check logs regularly

### Backup Before Housekeeping

```bash
# Automatic backup before cleanup
python manage.py dumpdata > backup_$(date +%Y%m%d).json
python manage.py run_housekeeping
```

## Summary

🎯 **Purpose**: Automated database maintenance  
⏰ **Schedule**: Daily, weekly, and every 6 hours  
🛠️ **Control**: CLI commands + web dashboard  
🔒 **Security**: Admin-only access  
📊 **Monitoring**: Logs + statistics  

The scheduler runs automatically - set it and forget it! ✨

---

For detailed documentation, see: [SCHEDULER-TASKS.md](SCHEDULER-TASKS.md)
