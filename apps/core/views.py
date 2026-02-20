from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


# Create your views here.


def profile(request):
    # Legacy core profile view now forwards to the users app profile
    if request.user.is_authenticated:
        return redirect('users:profile')
    messages.error(request, "Please login to access your profile.")
    return redirect('account_login')


def update_profile(request):
    # Forward old update endpoint to the new users profile edit view
    if request.user.is_authenticated:
        return redirect('users:profile_edit')
    messages.error(request, "Please login to edit your profile.")
    return redirect('account_login')


def save_profile(request):
    # This endpoint is deprecated; always forward to the new profile edit flow
    if not request.user.is_authenticated:
        messages.error(request, "Please login to access your profile.")
        return redirect('account_login')

    messages.info(request, "The profile form has moved. Please use the new edit page.")
    return redirect('users:profile_edit')