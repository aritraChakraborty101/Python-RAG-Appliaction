"""
Test script to verify scheduler functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from chat.scheduler import start_scheduler, get_scheduled_jobs
from chat.tasks import generate_statistics
import time

print("=" * 80)
print("Testing APScheduler Integration")
print("=" * 80)

# Start the scheduler
print("\n1. Starting scheduler...")
scheduler = start_scheduler()
print("✓ Scheduler started successfully!")

# Get scheduled jobs
print("\n2. Fetching scheduled jobs...")
jobs = get_scheduled_jobs()
print(f"✓ Found {len(jobs)} scheduled jobs:")

for i, job in enumerate(jobs, 1):
    print(f"\n   Job #{i}:")
    print(f"   - ID: {job['id']}")
    print(f"   - Name: {job['name']}")
    print(f"   - Next Run: {job['next_run_time']}")
    print(f"   - Trigger: {job['trigger']}")

# Test manual task execution
print("\n3. Testing manual task execution...")
stats = generate_statistics()
print("✓ Statistics generated:")
print(f"   - Total Users: {stats['total_users']}")
print(f"   - Total Conversations: {stats['total_conversations']}")
print(f"   - Total Messages: {stats['total_messages']}")
print(f"   - Recent Messages (24h): {stats['recent_messages_24h']}")

print("\n" + "=" * 80)
print("Scheduler Test Completed Successfully! ✓")
print("=" * 80)

print("\nThe scheduler will continue running in the background.")
print("In production, it starts automatically with Django server.")
print("\nTo stop: Press Ctrl+C")

# Keep script running for a bit to show scheduler is active
try:
    time.sleep(5)
except KeyboardInterrupt:
    print("\nShutting down...")
