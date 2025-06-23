from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import *
from .forms import *

def home(request):
    """Page d'accueil"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'services': Service.objects.filter(is_active=True)[:6],
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """Dashboard client"""
    user = request.user
    profile = user.profile
    
    # Statistiques utilisateur
    recent_orders = user.orders.all()[:5]
    total_orders = user.orders.count()
    total_spent = user.orders.filter(status='completed').aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    # Notifications non lues
    unread_notifications = user.notifications.filter(is_read=False)[:5]
    
    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'unread_notifications': unread_notifications,
        'unread_count': unread_notifications.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Dashboard administrateur"""
    if not request.user.is_staff:
        return redirect('dashboard')
    
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    # KPIs du jour
    today_orders = Order.objects.filter(created_at__date=today)
    today_revenue = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Comparaison avec hier
    yesterday_orders = Order.objects.filter(created_at__date=yesterday)
    yesterday_revenue = yesterday_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Calcul des pourcentages
    orders_change = ((today_orders.count() - yesterday_orders.count()) / 
                    max(yesterday_orders.count(), 1)) * 100
    revenue_change = ((today_revenue - yesterday_revenue) / 
                     max(yesterday_revenue, 1)) * 100
    
    # Statut des imprimantes
    printers = Printer.objects.all()
    
    # Commandes récentes
    recent_orders = Order.objects.select_related('customer', 'service', 'printer')[:10]
    
    # Alertes
    alerts = []
    for printer in printers:
        if printer.status == 'offline':
            alerts.append({
                'type': 'critical',
                'title': f'Imprimante {printer.name} hors ligne',
                'message': 'L\'imprimante ne répond plus',
                'time': 'Il y a 15 min'
            })
        elif printer.toner_level < 20:
            alerts.append({
                'type': 'warning',
                'title': f'Niveau de toner faible - {printer.name}',
                'message': f'Toner à {printer.toner_level}%',
                'time': 'Il y a 1h'
            })
    
    context = {
        'today_orders_count': today_orders.count(),
        'today_revenue': today_revenue,
        'orders_change': orders_change,
        'revenue_change': revenue_change,
        'avg_process_time': 12,  # À calculer dynamiquement
        'active_alerts': len(alerts),
        'printers': printers,
        'recent_orders': recent_orders,
        'alerts': alerts[:3],
        'pages_count': sum(p.total_pages_printed for p in printers),
        'completed_orders': today_orders.filter(status='completed').count(),
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def new_order(request):
    """Créer une nouvelle commande"""
    if request.method == 'POST':
        # Traitement du formulaire de commande
        service_id = request.POST.get('service')
        quantity = int(request.POST.get('quantity', 1))
        
        service = get_object_or_404(Service, id=service_id)
        
        # Calcul du prix
        base_price = service.base_price
        options_price = 0
        
        # Options sélectionnées
        selected_options = []
        for key, value in request.POST.items():
            if key.startswith('option_'):
                option_id = key.replace('option_', '')
                option = ServiceOption.objects.get(id=option_id)
                selected_options.append(option)
                options_price += option.price
        
        subtotal = (base_price + options_price) * quantity
        
        # Remise étudiant
        discount = 0
        if request.user.profile.is_verified_student:
            discount = subtotal * request.user.profile.get_student_discount()
        
        total = subtotal - discount
        
        # Création de la commande
        order = Order.objects.create(
            customer=request.user,
            service=service,
            quantity=quantity,
            base_price=base_price,
            options_price=options_price,
            subtotal=subtotal,
            discount_amount=discount,
            total_amount=total,
            special_instructions=request.POST.get('instructions', '')
        )
        
        # Ajout des options
        for option in selected_options:
            OrderOption.objects.create(
                order=order,
                option=option,
                price=option.price
            )
        
        messages.success(request, f'Commande {order.order_number} créée avec succès!')
        return redirect('order_detail', order_id=order.id)
    
    services = Service.objects.filter(is_active=True)
    context = {'services': services}
    return render(request, 'orders/new_order.html', context)

@login_required
def configure_order(request, service_id):
    """Configuration des options de commande"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    # Grouper les options par groupe
    options_by_group = {}
    for option in service.options.all():
        if option.option_group not in options_by_group:
            options_by_group[option.option_group] = []
        options_by_group[option.option_group].append(option)
    
    context = {
        'service': service,
        'options_by_group': options_by_group,
    }
    return render(request, 'orders/configure.html', context)

@login_required
def order_confirmation(request):
    """Confirmation de commande"""
    if request.method == 'POST':
        # Récupération des données de session ou POST
        order_data = request.session.get('order_data', {})
        
        # Traitement de la confirmation
        if 'confirm' in request.POST:
            # Créer la commande définitive
            # ... logique de création
            messages.success(request, 'Commande confirmée avec succès!')
            return redirect('dashboard')
    
    return render(request, 'orders/confirmation.html')

@login_required
def my_orders(request):
    """Liste des commandes de l'utilisateur"""
    orders = request.user.orders.select_related('service', 'printer')
    
    # Filtres
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(service__name__icontains=search)
        )
    
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/my_orders.html', context)

@login_required
def order_detail(request, order_id):
    """Détail d'une commande"""
    order = get_object_or_404(Order, id=order_id)
    
    # Vérifier que l'utilisateur peut voir cette commande
    if not request.user.is_staff and order.customer != request.user:
        messages.error(request, "Vous n'avez pas accès à cette commande.")
        return redirect('my_orders')
    
    context = {'order': order}
    return render(request, 'orders/detail.html', context)

@login_required
def credits_management(request):
    """Gestion des crédits"""
    profile = request.user.profile
    transactions = request.user.transactions.all()[:10]
    
    if request.method == 'POST':
        form = CreditRechargeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            
            # Traitement du rechargement
            profile.credits_balance += amount
            profile.save()
            
            # Créer la transaction
            Transaction.objects.create(
                user=request.user,
                transaction_type='credit',
                payment_method=payment_method,
                amount=amount,
                description=f'Recharge {payment_method}',
                reference=f'CR-{timezone.now().strftime("%Y%m%d%H%M%S")}',
                balance_after=profile.credits_balance
            )
            
            messages.success(request, f'Compte rechargé de {amount} FCFA!')
            return redirect('credits_management')
    else:
        form = CreditRechargeForm()
    
    context = {
        'profile': profile,
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'credits/management.html', context)

@login_required
def profile_management(request):
    """Gestion du profil utilisateur"""
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('profile_management')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile/management.html', context)

# Vues AJAX pour l'admin
@login_required
def ajax_printer_status(request):
    """API AJAX pour le statut des imprimantes"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    printers = Printer.objects.all()
    data = []
    
    for printer in printers:
        data.append({
            'id': printer.id,
            'name': printer.name,
            'status': printer.status,
            'toner_level': printer.toner_level,
            'current_jobs': printer.current_jobs,
        })
    
    return JsonResponse({'printers': data})

@login_required
def ajax_order_stats(request):
    """API AJAX pour les statistiques de commandes"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today)
    
    stats = {
        'today_orders': orders_today.count(),
        'revenue_today': orders_today.aggregate(total=Sum('total_amount'))['total'] or 0,
        'pending_orders': Order.objects.filter(status='pending').count(),
        'printing_orders': Order.objects.filter(status='printing').count(),
    }
    
    return JsonResponse(stats)