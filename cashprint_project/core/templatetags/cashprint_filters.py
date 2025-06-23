from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie une valeur par un argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value):
    """Convertit un decimal en pourcentage"""
    try:
        return int(float(value) * 100)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency(value, currency_symbol="FCFA"):
    """Formate une valeur comme une devise"""
    try:
        return f"{int(float(value)):,} {currency_symbol}".replace(',', ' ')
    except (ValueError, TypeError):
        return f"0 {currency_symbol}"

@register.filter
def phone_format(value):
    """Formate un numéro de téléphone"""
    if not value:
        return ""
    
    # Convertir en string et nettoyer
    phone = str(value).strip()
    
    # Si commence par +237, garder tel quel
    if phone.startswith('+237'):
        return phone
    
    # Si commence par 237, ajouter +
    if phone.startswith('237'):
        return f"+{phone}"
    
    # Si commence par 6, ajouter +237
    if phone.startswith('6') and len(phone) == 9:
        return f"+237{phone}"
    
    return phone

@register.filter
def badge_color(status):
    """Retourne une classe CSS pour le statut"""
    status_colors = {
        'pending': 'warning',
        'confirmed': 'info',
        'printing': 'primary',
        'completed': 'success',
        'delivered': 'success',
        'cancelled': 'danger',
    }
    return status_colors.get(status, 'secondary')

@register.filter
def priority_color(priority):
    """Retourne une classe CSS pour la priorité"""
    priority_colors = {
        'low': 'success',
        'normal': 'info',
        'high': 'warning',
        'urgent': 'danger',
    }
    return priority_colors.get(priority, 'secondary')

@register.filter
def message_color(message_tag):
    """Retourne la classe Bootstrap pour les messages"""
    message_colors = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info',
        'debug': 'secondary',
    }
    return message_colors.get(message_tag, 'primary')

@register.simple_tag
def student_discount_percentage():
    """Tag pour afficher le pourcentage de remise étudiant"""
    from django.conf import settings
    discount = settings.CASHPRINT_SETTINGS.get('STUDENT_DISCOUNT', 0)
    return int(discount * 100)

@register.inclusion_tag('includes/status_badge.html')
def status_badge(status, status_display=None):
    """Tag d'inclusion pour afficher un badge de statut"""
    return {
        'status': status,
        'status_display': status_display or status,
        'badge_class': badge_color(status)
    }

@register.inclusion_tag('includes/price_display.html')
def price_display(amount, currency="FCFA", size="normal"):
    """Tag d'inclusion pour afficher un prix formaté"""
    return {
        'amount': amount,
        'currency': currency,
        'size': size,
        'formatted_amount': currency(amount, currency)
    }