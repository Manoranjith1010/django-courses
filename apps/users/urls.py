"""
User URL Configuration

URL patterns for user-related views.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]
