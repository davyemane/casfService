from django.conf import settings

def global_context(request):
    """Context global pour tous les templates"""
    context = {
        'COMPANY_NAME': settings.CASHPRINT_SETTINGS.get('COMPANY_NAME', 'Cash Print'),
        'COMPANY_ADDRESS': settings.CASHPRINT_SETTINGS.get('COMPANY_ADDRESS', ''),
        'COMPANY_PHONE': settings.CASHPRINT_SETTINGS.get('COMPANY_PHONE', ''),
        'CASHPRINT_SETTINGS': settings.CASHPRINT_SETTINGS,
    }
    
    if request.user.is_authenticated:
        # Notifications non lues (supposant que la relation s'appelle 'notifications')
        unread_notifications = request.user.notifications.filter(is_read=False)[:5]
        context.update({
            'unread_notifications': unread_notifications,
            'unread_count': unread_notifications.count(),
            'user_profile': getattr(request.user, 'profile', None),
        })

    return context
