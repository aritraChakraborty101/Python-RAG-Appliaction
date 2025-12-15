from django.db import models
from django.contrib.auth.models import User
import uuid


class EmailVerification(models.Model):
    """
    Model to store email verification tokens for users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"
    
    class Meta:
        verbose_name = "Email Verification"
        verbose_name_plural = "Email Verifications"
