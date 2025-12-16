from django.urls import path
from .views import (
    chat, 
    chat_history, 
    chat_page,
    conversations_list,
    conversation_detail,
    conversation_delete,
    conversation_rename
)

urlpatterns = [
    path('chat', chat, name='chat'),
    path('chat-history', chat_history, name='chat_history_list'),
    path('conversations', conversations_list, name='conversations_list'),
    path('conversations/<int:conversation_id>', conversation_detail, name='conversation_detail'),
    path('conversations/<int:conversation_id>/delete', conversation_delete, name='conversation_delete'),
    path('conversations/<int:conversation_id>/rename', conversation_rename, name='conversation_rename'),
]

# Web page URLs (not under /api/)
web_urlpatterns = [
    path('chat-page', chat_page, name='chat_page'),
]
