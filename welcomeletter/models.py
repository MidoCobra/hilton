from django.db import models


class ExternalLink(models.Model):
    """Model for managing external links and PDFs"""
    
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant Menu'),
        # ('spa', 'Spa Menu'),
        ('room_dining', 'In-Room Dining'),
        ('transfer', 'Transfer Service'),
        # ('board_menu', 'Board Menu'),
        ('info', 'Info Page Link'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text="Display name for the link")
    slug = models.SlugField(unique=True, help_text="Unique identifier for template usage")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    url = models.URLField(max_length=500, help_text="External URL or PDF link")
    description = models.TextField(blank=True, help_text="Optional description")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'External Link'
        verbose_name_plural = 'External Links'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Restaurant(models.Model):
    """Model for restaurant information"""
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, help_text="External image URL (for demo)")
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True, help_text="Uploaded restaurant image")
    menu_link = models.ForeignKey(
        ExternalLink, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='restaurants'
    )
    menu_pdf = models.FileField(upload_to='restaurants/menus/', blank=True, null=True, help_text="Upload restaurant menu PDF")
    
    # Social Media Links
    facebook_url = models.URLField(max_length=500, blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(max_length=500, blank=True, help_text="Instagram page URL")
    tiktok_url = models.URLField(max_length=500, blank=True, help_text="TikTok page URL")
    
    # Reservation Email
    email = models.EmailField(max_length=254, blank=True, help_text="Reservation email address")
    
    # Additional Information
    opening_hours = models.CharField(max_length=200, blank=True, help_text="e.g., 12:00 PM - 11:00 PM")
    location = models.CharField(max_length=500, blank=True, help_text="Restaurant location/floor information")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class TransferOption(models.Model):
    """Model for transfer/parking options"""
    
    name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    max_capacity = models.CharField(max_length=100, blank=True)
    price_to_hotel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_from_hotel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    icon = models.CharField(max_length=10, default='🚗', help_text="Emoji icon")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Transfer Option'
        verbose_name_plural = 'Transfer Options'
    
    def __str__(self):
        return self.name


class MailingListSubscriber(models.Model):
    """Model for mailing list subscribers"""
    
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Mailing List Subscriber'
        verbose_name_plural = 'Mailing List Subscribers'
    
    def __str__(self):
        return self.email


class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""
    
    # Contact Information
    phone_number = models.CharField(max_length=50, default='+20 2 2795 0000')
    whatsapp_number = models.CharField(max_length=50, default='+20 10 700 4785')
    email = models.EmailField(default='restaurant.ramses@hilton.com')
    
    # Social Links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Other Links
    hilton_honors_url = models.URLField(default='https://www.hilton.com/en/hilton-honors/member-benefits/')
    hilton_honors_join_url = models.URLField(default='https://www.hilton.com/en/hilton-honors/join/')
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return "Site Settings"
