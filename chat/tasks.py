"""
Scheduled background tasks for the chat application.
Handles periodic cleanup and housekeeping operations.
"""
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Conversation, ChatMessage
import logging

logger = logging.getLogger(__name__)


def delete_old_conversations():
    """
    Delete conversations and their messages older than 30 days.
    This helps maintain database size and remove stale data.
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=30)
        old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
        
        count = old_conversations.count()
        if count > 0:
            logger.info(f"Deleting {count} conversations older than 30 days")
            old_conversations.delete()
            logger.info(f"Successfully deleted {count} old conversations")
        else:
            logger.info("No old conversations to delete")
            
        return count
    except Exception as e:
        logger.error(f"Error deleting old conversations: {str(e)}")
        return 0


def cleanup_orphaned_messages():
    """
    Remove any ChatMessages that are not associated with a Conversation.
    This handles data integrity issues.
    """
    try:
        orphaned = ChatMessage.objects.filter(conversation__isnull=True)
        count = orphaned.count()
        
        if count > 0:
            logger.info(f"Cleaning up {count} orphaned messages")
            orphaned.delete()
            logger.info(f"Successfully cleaned up {count} orphaned messages")
        else:
            logger.info("No orphaned messages to clean up")
            
        return count
    except Exception as e:
        logger.error(f"Error cleaning up orphaned messages: {str(e)}")
        return 0


def cleanup_inactive_users():
    """
    Delete users who registered but never verified their email (inactive for 7+ days).
    This keeps the user database clean.
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=7)
        inactive_users = User.objects.filter(
            is_active=False,
            date_joined__lt=cutoff_date
        )
        
        count = inactive_users.count()
        if count > 0:
            logger.info(f"Deleting {count} inactive users")
            inactive_users.delete()
            logger.info(f"Successfully deleted {count} inactive users")
        else:
            logger.info("No inactive users to delete")
            
        return count
    except Exception as e:
        logger.error(f"Error deleting inactive users: {str(e)}")
        return 0


def generate_statistics():
    """
    Generate and log usage statistics for monitoring.
    This helps track application health and usage patterns.
    """
    try:
        total_users = User.objects.filter(is_active=True).count()
        total_conversations = Conversation.objects.count()
        total_messages = ChatMessage.objects.count()
        
        # Recent activity (last 24 hours)
        last_24h = timezone.now() - timedelta(hours=24)
        recent_conversations = Conversation.objects.filter(created_at__gte=last_24h).count()
        recent_messages = ChatMessage.objects.filter(timestamp__gte=last_24h).count()
        
        stats = {
            'total_users': total_users,
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'recent_conversations_24h': recent_conversations,
            'recent_messages_24h': recent_messages,
        }
        
        logger.info(f"System Statistics: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error generating statistics: {str(e)}")
        return {}


def run_all_housekeeping_tasks():
    """
    Master function that runs all housekeeping tasks in sequence.
    This is the main scheduled task.
    """
    logger.info("=" * 60)
    logger.info("Starting scheduled housekeeping tasks")
    logger.info("=" * 60)
    
    # Task 1: Delete old conversations
    deleted_conversations = delete_old_conversations()
    
    # Task 2: Clean up orphaned messages
    cleaned_messages = cleanup_orphaned_messages()
    
    # Task 3: Remove inactive users
    deleted_users = cleanup_inactive_users()
    
    # Task 4: Generate statistics
    stats = generate_statistics()
    
    logger.info("=" * 60)
    logger.info("Housekeeping tasks completed")
    logger.info(f"Summary: {deleted_conversations} conversations, "
                f"{cleaned_messages} orphaned messages, "
                f"{deleted_users} inactive users removed")
    logger.info("=" * 60)
    
    return {
        'deleted_conversations': deleted_conversations,
        'cleaned_messages': cleaned_messages,
        'deleted_users': deleted_users,
        'stats': stats
    }
