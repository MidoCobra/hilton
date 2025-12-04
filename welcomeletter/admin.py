from django.contrib import admin
from .models import ExternalLink, Restaurant, TransferOption, MailingListSubscriber, SiteSettings


@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'slug', 'url']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category', 'name']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'menu_link', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image_url', 'image')
        }),
        ('Links & Media', {
            'fields': ('menu_link', 'facebook_url', 'instagram_url', 'tiktok_url')
        }),
        ('Contact & Location', {
            'fields': ('email', 'opening_hours', 'location')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(TransferOption)
class TransferOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'max_capacity', 'price_to_hotel', 'price_from_hotel', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'vehicle_type']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']


@admin.register(MailingListSubscriber)
class MailingListSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'ip_address']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    ordering = ['-subscribed_at']
    readonly_fields = ['subscribed_at', 'ip_address']
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = "Deactivate selected subscribers"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Information', {
            'fields': ('phone_number', 'whatsapp_number', 'email')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        }),
        ('Hilton Links', {
            'fields': ('hilton_honors_url', 'hilton_honors_join_url')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
