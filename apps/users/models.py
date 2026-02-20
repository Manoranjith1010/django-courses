"""
Custom User Models

This module contains custom user-related models.
For a custom user model, uncomment and extend AbstractUser.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# =============================================================================
# CUSTOM USER MODEL (Optional - uncomment to use)
# =============================================================================
# class CustomUser(AbstractUser):
#     """
#     Custom user model for extended user functionality.
#     
#     To use this model:
#     1. Uncomment this class
#     2. Add AUTH_USER_MODEL = 'users.CustomUser' to settings.py
#     3. Run makemigrations and migrate
#     """
#     # Additional fields
#     bio = models.TextField(_('bio'), max_length=500, blank=True)
#     avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
#     phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
#     date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
#     
#     # Profile settings
#     email_notifications = models.BooleanField(_('email notifications'), default=True)
#     is_instructor = models.BooleanField(_('instructor status'), default=False)
#     
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#     
#     def __str__(self):
#         return self.email or self.username


class UserProfile(models.Model):
    """
    Extended user profile for additional user data.
    Links to the default Django User model via OneToOne relationship.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile'  # Unique related_name to avoid conflict with core.Profile
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    
    # Learning preferences
    preferred_language = models.CharField(
        _('preferred language'),
        max_length=10,
        default='en'
    )
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"Profile for {self.user.username}"
