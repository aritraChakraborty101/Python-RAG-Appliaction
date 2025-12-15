from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/auth/signup-page', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
