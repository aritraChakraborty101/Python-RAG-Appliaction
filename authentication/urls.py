from django.urls import path
from .views import signup, signup_page

urlpatterns = [
    path('signup', signup, name='signup'),
    path('signup-page', signup_page, name='signup_page'),
]
