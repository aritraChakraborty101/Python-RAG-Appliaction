# Scheduler Quick Reference Card

## 🚀 Quick Commands

```bash
# View scheduler status and jobs
python manage.py scheduler_info

# Run all housekeeping tasks
python manage.py run_housekeeping

# Run specific task
python manage.py run_housekeeping --task conversations  # Delete old conversations
python manage.py run_housekeeping --task messages       # Cleanup orphaned messages
python manage.py run_housekeeping --task users          # Remove inactive users
python manage.py run_housekeeping --task stats          # Generate statistics

# Test scheduler
python test_scheduler.py
```

## 📅 Default Schedule

| Task | When | What |
|------|------|------|
| **Daily Housekeeping** | 2:00 AM daily | All cleanup tasks |
| **Weekly Cleanup** | Sunday 3:00 AM | Delete conversations 30+ days old |
| **Statistics** | Every 6 hours | Generate usage stats |

## 🌐 Web Dashboard

**URL**: http://127.0.0.1:8000/scheduler-admin

**Features**:
- 📊 Live statistics (users, conversations, messages, activity)
- ⚡ Manual task triggers (one-click execution)
- 📅 View scheduled jobs and next run times
- 🔄 Auto-refresh every 30 seconds

**Requirements**: Admin/superuser account

## 🔌 API Endpoints (Admin Only)

```bash
# Get scheduler status
GET /api/admin/scheduler/status

# Trigger task manually
POST /api/admin/scheduler/trigger
Body: {"task": "all|conversations|messages|users|stats"}

# Get system statistics
GET /api/admin/scheduler/statistics
```

**Authorization**: `Bearer <jwt_token>` (admin user required)

## 📋 Task Details

| Task | Retention | Description |
|------|-----------|-------------|
| `delete_old_conversations()` | 30 days | Remove old conversations & messages |
| `cleanup_orphaned_messages()` | N/A | Fix data integrity issues |
| `cleanup_inactive_users()` | 7 days | Remove unverified users |
| `generate_statistics()` | N/A | Track system usage |
| `run_all_housekeeping_tasks()` | N/A | Execute all tasks |

## 🛠️ Customization

**Change Schedule Time** (`chat/scheduler.py`):
```python
# Line ~35: Change daily housekeeping time
trigger=CronTrigger(hour=3, minute=30)  # 3:30 AM
```

**Change Retention Period** (`chat/tasks.py`):
```python
# Line ~16: Change conversation retention
cutoff_date = timezone.now() - timedelta(days=60)  # 60 days
```

**Enable Test Mode** (`chat/scheduler.py`):
```python
# Uncomment lines 61-68 for 5-minute interval testing
scheduler.add_job(
    run_all_housekeeping_tasks,
    trigger=IntervalTrigger(minutes=5),
    ...
)
```

## 🔍 Troubleshooting

**Scheduler Not Starting?**
```bash
# Check if server is running
python manage.py runserver

# Test manually
python test_scheduler.py

# Verify APScheduler installed
pip show apscheduler
```

**Tasks Not Running?**
```bash
# View scheduler status
python manage.py scheduler_info

# Check for errors
python manage.py runserver  # Watch console

# Test manually
python manage.py run_housekeeping
```

**Dashboard Shows 403?**
```bash
# Create superuser
python manage.py createsuperuser

# Login at: http://127.0.0.1:8000/api/auth/login
# Then access: http://127.0.0.1:8000/scheduler-admin
```

## 📊 Expected Output Examples

**Scheduler Info:**
```
APScheduler Status
==================
Scheduler State: 1
Total Scheduled Jobs: 3

Job #1: Daily Housekeeping Tasks
Next Run: 2025-12-17 02:00:00
```

**Run Housekeeping:**
```
Running Housekeeping Tasks
==========================
Deleted: 5 conversations, 2 messages, 1 users
Stats: {total_users: 42, total_messages: 892}
```

**Test Scheduler:**
```
Testing APScheduler Integration
===============================
✓ Scheduler started successfully!
✓ Found 3 scheduled jobs
✓ Statistics generated
```

## 📚 Documentation Links

- **[QUICKSTART-SCHEDULER.md](QUICKSTART-SCHEDULER.md)** - 5-minute quick start
- **[SCHEDULER-TASKS.md](SCHEDULER-TASKS.md)** - Complete documentation
- **[IMPLEMENTATION-SUMMARY.md](IMPLEMENTATION-SUMMARY.md)** - Technical details
- **[README.md](README.md)** - Main project documentation

## ✅ Health Check

Run this to verify everything is working:

```bash
# 1. Install dependencies
pip install apscheduler

# 2. Run migrations
python manage.py migrate

# 3. Test scheduler
python test_scheduler.py

# 4. View status
python manage.py scheduler_info

# 5. Run manual task
python manage.py run_housekeeping --task stats

# 6. Start server (scheduler auto-starts)
python manage.py runserver
```

If all commands succeed, the scheduler is working! ✨

## 🎯 Quick Stats

- **Files Created**: 11
- **API Endpoints**: 3 admin endpoints
- **CLI Commands**: 2 management commands
- **Scheduled Jobs**: 3 default schedules
- **Task Functions**: 5 housekeeping tasks
- **Documentation Pages**: 4 comprehensive guides

---

**Need Help?** Check the full documentation in [SCHEDULER-TASKS.md](SCHEDULER-TASKS.md)
