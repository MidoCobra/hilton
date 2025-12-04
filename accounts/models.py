from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager using email as username"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email as username"""
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the primary identifier.
    Extends Django's AbstractBaseUser and PermissionsMixin for full auth compatibility.
    """
    
    # Primary identifier
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=254, unique=True)  # Also set to email for consistency
    
    # Profile Information
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # User Preferences
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    newsletter_subscription = models.BooleanField(default=False, help_text="Subscribe to newsletter")
    
    # Account Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into the admin site")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Manager
    objects = CustomUserManager()
    
    # Use email as the primary username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-date_joined']),
        ]
    
    def __str__(self):
        """Return user's display name or email"""
        return self.get_display_name() or self.email
    
    def get_full_name(self):
        """Return user's full name"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name
    
    def get_display_name(self):
        """Return display name, preferring full name"""
        full_name = self.get_full_name()
        return full_name if full_name else self.email
    
    def get_short_name(self):
        """Return user's first name"""
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user"""
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)
