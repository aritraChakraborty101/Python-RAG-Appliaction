"""
Django management command to manually run housekeeping tasks.
Usage: python manage.py run_housekeeping [--task TASK_NAME]
"""
from django.core.management.base import BaseCommand
from chat.tasks import (
    run_all_housekeeping_tasks,
    delete_old_conversations,
    cleanup_orphaned_messages,
    cleanup_inactive_users,
    generate_statistics
)


class Command(BaseCommand):
    help = 'Run housekeeping tasks manually'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--task',
            type=str,
            choices=['all', 'conversations', 'messages', 'users', 'stats'],
            default='all',
            help='Specific task to run (default: all)'
        )
    
    def handle(self, *args, **options):
        task = options['task']
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Running Housekeeping Tasks'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if task == 'all':
            result = run_all_housekeeping_tasks()
            self.stdout.write(self.style.SUCCESS(
                f"\nDeleted: {result['deleted_conversations']} conversations, "
                f"{result['cleaned_messages']} orphaned messages, "
                f"{result['deleted_users']} inactive users"
            ))
            self.stdout.write(self.style.SUCCESS(f"Stats: {result['stats']}"))
            
        elif task == 'conversations':
            count = delete_old_conversations()
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} old conversations"))
            
        elif task == 'messages':
            count = cleanup_orphaned_messages()
            self.stdout.write(self.style.SUCCESS(f"Cleaned {count} orphaned messages"))
            
        elif task == 'users':
            count = cleanup_inactive_users()
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} inactive users"))
            
        elif task == 'stats':
            stats = generate_statistics()
            self.stdout.write(self.style.SUCCESS(f"Statistics: {stats}"))
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Housekeeping completed successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
