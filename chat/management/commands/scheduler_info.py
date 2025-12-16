"""
Django management command to view scheduler status and jobs.
Usage: python manage.py scheduler_info
"""
from django.core.management.base import BaseCommand
from chat.scheduler import get_scheduled_jobs, scheduler
from django.utils import timezone


class Command(BaseCommand):
    help = 'Display scheduler status and scheduled jobs'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('APScheduler Status'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        
        if scheduler is None:
            self.stdout.write(self.style.ERROR('Scheduler is not running!'))
            self.stdout.write(self.style.WARNING(
                'The scheduler should start automatically when you run: python manage.py runserver'
            ))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Scheduler State: {scheduler.state}'))
        self.stdout.write(self.style.SUCCESS(f'Current Time: {timezone.now()}'))
        self.stdout.write('')
        
        jobs = get_scheduled_jobs()
        
        if not jobs:
            self.stdout.write(self.style.WARNING('No scheduled jobs found'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Total Scheduled Jobs: {len(jobs)}'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        
        for i, job in enumerate(jobs, 1):
            self.stdout.write(self.style.SUCCESS(f'\nJob #{i}:'))
            self.stdout.write(f"  ID: {job['id']}")
            self.stdout.write(f"  Name: {job['name']}")
            self.stdout.write(f"  Next Run: {job['next_run_time']}")
            self.stdout.write(f"  Trigger: {job['trigger']}")
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 80))
