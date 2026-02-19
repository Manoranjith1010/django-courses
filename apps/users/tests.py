"""
User Tests

Test cases for user-related functionality.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class UserProfileModelTest(TestCase):
    """Tests for the UserProfile model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Test that a profile can be created for a user."""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), f"Profile for {self.user.username}")
    
    def test_profile_defaults(self):
        """Test profile default values."""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.preferred_language, 'en')
        self.assertTrue(profile.email_notifications)


class UserViewsTest(TestCase):
    """Tests for user views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication."""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
