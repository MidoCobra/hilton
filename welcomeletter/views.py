from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import ExternalLink, Restaurant, TransferOption, MailingListSubscriber, SiteSettings


def get_common_context():
    """Get common context data for all pages"""
    return {
        'settings': SiteSettings.get_settings(),
        'external_links': {link.slug: link for link in ExternalLink.objects.filter(is_active=True)},
    }


def home(request):
    """Welcome Letter page - main landing page"""
    context = get_common_context()
    return render(request, 'home.html', context)


def transfers(request):
    """Transfers & Parking page"""
    context = get_common_context()
    context['transfer_options'] = TransferOption.objects.filter(is_active=True)
    return render(request, 'transfers.html', context)


def info(request):
    """Important Information page"""
    context = get_common_context()
    # Get room dining menu link
    context['room_dining_link'] = ExternalLink.objects.filter(
        category='room_dining', is_active=True
    ).first()
    # Get info page specific link
    context['info_link'] = ExternalLink.objects.filter(
        category='info', is_active=True
    ).first()
    return render(request, 'info.html', context)


def restaurants(request):
    """Restaurants & Bars page"""
    context = get_common_context()
    context['restaurants'] = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants.html', context)


def kids(request):
    """Kids & Family page"""
    context = get_common_context()
    return render(request, 'kids.html', context)


def spa(request):
    """The Spa page"""
    context = get_common_context()
    context['spa_menu_link'] = ExternalLink.objects.filter(
        slug='spa-menu', is_active=True
    ).first()
    return render(request, 'spa.html', context)


def board_menus(request):
    """Half & Full Board Menus page"""
    context = get_common_context()
    # Get restaurants that have board menus
    context['restaurants'] = Restaurant.objects.filter(is_active=True)
    return render(request, 'board_menus.html', context)


def hilton_honors(request):
    """Hilton Honors Benefits page"""
    context = get_common_context()
    return render(request, 'hilton_honors.html', context)


@require_POST
def subscribe_newsletter(request):
    """Handle newsletter subscription"""
    email = request.POST.get('email', '').strip().lower()
    
    if not email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Please enter your email address.'})
        messages.error(request, 'Please enter your email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Basic email validation
    if '@' not in email or '.' not in email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
        messages.error(request, 'Please enter a valid email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Check if already subscribed
    subscriber, created = MailingListSubscriber.objects.get_or_create(
        email=email,
        defaults={'ip_address': ip_address, 'is_active': True}
    )
    
    if not created:
        if subscriber.is_active:
            message = 'You are already subscribed to our mailing list!'
        else:
            # Reactivate subscription
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()
            message = 'Welcome back! Your subscription has been reactivated.'
    else:
        message = 'Thank you for subscribing to our mailing list!'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': message})
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', '/'))
