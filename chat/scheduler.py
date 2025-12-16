"""
APScheduler configuration for background tasks.
Manages periodic task execution using BackgroundScheduler.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def start_scheduler():
    """
    Initialize and start the APScheduler background scheduler.
    This should be called once when Django starts.
    """
    global scheduler
    
    if scheduler is not None:
        logger.warning("Scheduler already running")
        return scheduler
    
    logger.info("Initializing APScheduler...")
    
    scheduler = BackgroundScheduler(
        timezone=settings.TIME_ZONE,
        daemon=True
    )
    
    # Import tasks here to avoid circular imports
    from .tasks import (
        run_all_housekeeping_tasks,
        delete_old_conversations,
        generate_statistics
    )
    
    # Schedule 1: Run all housekeeping tasks daily at 2:00 AM
    scheduler.add_job(
        run_all_housekeeping_tasks,
        trigger=CronTrigger(hour=2, minute=0),
        id='daily_housekeeping',
        name='Daily Housekeeping Tasks',
        replace_existing=True,
        max_instances=1
    )
    logger.info("Scheduled: Daily housekeeping at 2:00 AM")
    
    # Schedule 2: Delete old conversations weekly on Sunday at 3:00 AM
    scheduler.add_job(
        delete_old_conversations,
        trigger=CronTrigger(day_of_week='sun', hour=3, minute=0),
        id='weekly_cleanup',
        name='Weekly Conversation Cleanup',
        replace_existing=True,
        max_instances=1
    )
    logger.info("Scheduled: Weekly cleanup on Sunday at 3:00 AM")
    
    # Schedule 3: Generate statistics every 6 hours
    scheduler.add_job(
        generate_statistics,
        trigger=IntervalTrigger(hours=6),
        id='statistics_generation',
        name='Generate System Statistics',
        replace_existing=True,
        max_instances=1
    )
    logger.info("Scheduled: Statistics generation every 6 hours")
    
    # Optional: For testing, run housekeeping every 5 minutes (commented out)
    # Uncomment the following lines for testing purposes:
    """
    scheduler.add_job(
        run_all_housekeeping_tasks,
        trigger=IntervalTrigger(minutes=5),
        id='test_housekeeping',
        name='Test Housekeeping (Every 5 min)',
        replace_existing=True,
        max_instances=1
    )
    logger.info("Scheduled: Test housekeeping every 5 minutes")
    """
    
    scheduler.start()
    logger.info("APScheduler started successfully")
    
    return scheduler


def stop_scheduler():
    """
    Gracefully shutdown the scheduler.
    This should be called when Django is shutting down.
    """
    global scheduler
    
    if scheduler is not None:
        logger.info("Shutting down APScheduler...")
        scheduler.shutdown(wait=True)
        scheduler = None
        logger.info("APScheduler stopped")
    else:
        logger.warning("Scheduler is not running")


def get_scheduled_jobs():
    """
    Get list of all scheduled jobs with their details.
    Useful for monitoring and debugging.
    """
    global scheduler
    
    if scheduler is None:
        return []
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run_time': job.next_run_time,
            'trigger': str(job.trigger)
        })
    
    return jobs


def run_job_now(job_id):
    """
    Manually trigger a scheduled job immediately.
    Useful for testing and manual operations.
    """
    global scheduler
    
    if scheduler is None:
        logger.error("Scheduler is not running")
        return False
    
    try:
        job = scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=None)
            logger.info(f"Triggered job: {job_id}")
            return True
        else:
            logger.error(f"Job not found: {job_id}")
            return False
    except Exception as e:
        logger.error(f"Error triggering job {job_id}: {str(e)}")
        return False
