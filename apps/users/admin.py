from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    
    list_display = ('user', 'phone_number', 'email_notifications', 'created_at')
    list_filter = ('email_notifications', 'preferred_language', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'avatar', 'bio')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'date_of_birth')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'email_notifications')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# INLINE PROFILE IN USER ADMIN (Optional)
# =============================================================================
class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile to show in User admin."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# Uncomment to add profile inline to default User admin
# class CustomUserAdmin(BaseUserAdmin):
#     inlines = (UserProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
