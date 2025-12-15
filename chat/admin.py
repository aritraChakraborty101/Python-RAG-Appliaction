from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_message_preview', 'ai_response_preview', 'timestamp']
    list_filter = ['timestamp', 'user']
    search_fields = ['user__username', 'user_message', 'ai_response']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def user_message_preview(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    user_message_preview.short_description = 'User Message'
    
    def ai_response_preview(self, obj):
        return obj.ai_response[:50] + '...' if len(obj.ai_response) > 50 else obj.ai_response
    ai_response_preview.short_description = 'AI Response'
