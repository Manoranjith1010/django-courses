"""
User Views

This module contains views for user-related functionality.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import UserProfile

User = get_user_model()


@login_required
def profile_view(request):
    """Display the current user's profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit the current user's profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        profile.bio = request.POST.get('bio', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.preferred_language = request.POST.get('preferred_language', 'en')
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'users/profile_edit.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Class-based view for viewing a user's profile."""
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserProfile.objects.get_or_create(user=self.object)
        context['profile'] = profile
        return context
