from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom User Admin with email as primary username"""
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture', 'bio')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'newsletter_subscription')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name')
        }),
    )
    
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'email_notifications', 'newsletter_subscription', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']
    
    # Use email instead of username
    filter_horizontal = ('groups', 'user_permissions')
