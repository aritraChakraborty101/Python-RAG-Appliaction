from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    """
    Model to store chat messages between users and AI
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
