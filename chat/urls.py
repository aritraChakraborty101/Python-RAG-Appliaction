from django.urls import path
from .views import chat, chat_history, chat_page

urlpatterns = [
    path('chat', chat, name='chat'),
    path('chat-history', chat_history, name='chat_history_list'),
]

# Web page URLs (not under /api/)
web_urlpatterns = [
    path('chat-page', chat_page, name='chat_page'),
]
