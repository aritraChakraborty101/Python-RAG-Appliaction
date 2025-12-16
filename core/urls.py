from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from chat.urls import web_urlpatterns as chat_web_urls

urlpatterns = [
    path('', RedirectView.as_view(url='/api/auth/landing', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('chat.urls')),
] + chat_web_urls
