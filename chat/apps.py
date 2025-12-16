from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class ChatConfig(AppConfig):
    name = 'chat'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        """
        Initialize the scheduler when Django starts.
        This runs once per process.
        """
        import sys
        
        # Only start scheduler in the main process (not during migrations, etc.)
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            try:
                from .scheduler import start_scheduler
                start_scheduler()
                logger.info("Chat app scheduler initialized")
            except Exception as e:
                logger.error(f"Failed to start scheduler: {str(e)}")
