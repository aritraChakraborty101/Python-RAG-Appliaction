from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import signup, signup_page, login, login_page, dashboard, chat_history, protected_test

urlpatterns = [
    # Registration
    path('signup', signup, name='signup'),
    path('signup-page', signup_page, name='signup_page'),
    
    # JWT Authentication
    path('login', login, name='login'),
    path('login-page', login_page, name='login_page'),
    path('dashboard', dashboard, name='dashboard'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Protected Routes
    path('chat-history', chat_history, name='chat_history'),
    path('protected', protected_test, name='protected_test'),
]
