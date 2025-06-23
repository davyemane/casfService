from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion des commandes
    path('orders/new/', views.new_order, name='new_order'),
    path('orders/configure/<int:service_id>/', views.configure_order, name='configure_order'),
    path('orders/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    
    # Gestion des crédits
    path('credits/', views.credits_management, name='credits_management'),
    
    # Gestion du profil
    path('profile/', views.profile_management, name='profile_management'),
    
    # APIs AJAX pour l'administration
    path('ajax/printer-status/', views.ajax_printer_status, name='ajax_printer_status'),
    path('ajax/order-stats/', views.ajax_order_stats, name='ajax_order_stats'),
]