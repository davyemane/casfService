from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'credits_balance', 'is_verified_student', 'created_at']
    list_filter = ['user_type', 'is_verified_student', 'created_at']
    search_fields = ['user__username', 'user__email', 'student_id', 'institution']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'user_type', 'is_verified_student')
        }),
        ('Informations', {
            'fields': ('phone', 'student_id', 'institution', 'address')
        }),
        ('Crédits', {
            'fields': ('credits_balance',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'unit', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order'),
            total_revenue=Sum('order__total_amount')
        )

class ServiceOptionInline(admin.TabularInline):
    model = ServiceOption
    extra = 1

@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ['service', 'name', 'option_group', 'price', 'is_required', 'is_default']
    list_filter = ['service', 'option_group', 'is_required']
    search_fields = ['name', 'description']

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'status', 'toner_level', 'paper_level', 'current_jobs_count']
    list_filter = ['status', 'model']
    search_fields = ['name', 'model', 'location']
    
    def current_jobs_count(self, obj):
        return obj.current_jobs
    current_jobs_count.short_description = 'Travaux en cours'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('orders')

class OrderOptionInline(admin.TabularInline):
    model = OrderOption
    extra = 0
    readonly_fields = ['option', 'price']

class OrderFileInline(admin.TabularInline):
    model = OrderFile
    extra = 0
    readonly_fields = ['uploaded_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'service', 'status', 'priority', 'total_amount', 'created_at']
    list_filter = ['status', 'priority', 'service__category', 'created_at']
    search_fields = ['order_number', 'customer__username', 'customer__email']
    readonly_fields = ['order_number', 'created_at', 'confirmed_at', 'started_at', 'completed_at']
    inlines = [OrderOptionInline, OrderFileInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Commande', {
            'fields': ('order_number', 'customer', 'service', 'quantity')
        }),
        ('Prix', {
            'fields': ('base_price', 'options_price', 'subtotal', 'discount_amount', 'total_amount')
        }),
        ('Statut', {
            'fields': ('status', 'priority', 'printer')
        }),
        ('Instructions', {
            'fields': ('special_instructions',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'confirmed_at', 'started_at', 'completed_at', 'estimated_delivery'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'service', 'printer')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'payment_method', 'amount', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'payment_method', 'created_at']
    search_fields = ['user__username', 'reference', 'description']
    readonly_fields = ['reference', 'created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marquer comme lu"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Marquer comme non lu"

# Configuration de l'admin
admin.site.site_header = "Cash Print Administration"
admin.site.site_title = "Cash Print Admin"
admin.site.index_title = "Panneau d'administration"