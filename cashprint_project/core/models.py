
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from datetime import datetime

class UserProfile(models.Model):
    USER_TYPES = [
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
        ('company', 'Entreprise'),
        ('individual', 'Particulier'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='individual')
    phone = PhoneNumberField(blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    credits_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_verified_student = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_user_type_display()})"

    def get_student_discount(self):
        from django.conf import settings
        return settings.CASHPRINT_SETTINGS.get('STUDENT_DISCOUNT', 0.20) if self.is_verified_student else 0

class Service(models.Model):
    CATEGORIES = [
        ('impression', 'Impression Documents'),
        ('badges', 'Badges & Cartes'),
        ('signaletique', 'Signalétique'),
        ('textile', 'Textile & Vêtements'),
        ('objets', 'Objets Personnalisés'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50, default='unité')
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, default='fas fa-print')
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ServiceOption(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    option_group = models.CharField(max_length=50)  # format, couleur, papier, etc.
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_required = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"

class Printer(models.Model):
    STATUS_CHOICES = [
        ('online', 'En ligne'),
        ('offline', 'Hors ligne'),
        ('busy', 'Occupée'),
        ('maintenance', 'Maintenance'),
    ]
    
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    toner_level = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    paper_level = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    total_pages_printed = models.PositiveIntegerField(default=0)
    last_maintenance = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.model})"
    
    @property
    def current_jobs(self):
        return self.orders.filter(status__in=['pending', 'printing']).count()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('printing', 'En cours d\'impression'),
        ('completed', 'Terminée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('normal', 'Normale'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    printer = models.ForeignKey(Printer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    # Prix
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    options_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Statut et métadonnées
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.order_number} - {self.customer.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        today = datetime.now()
        prefix = f"CP-{today.year}"
        last_order = Order.objects.filter(order_number__startswith=prefix).order_by('-created_at').first()
        
        if last_order:
            last_number = int(last_order.order_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
            
        return f"{prefix}-{new_number:06d}"

class OrderOption(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='selected_options')
    option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.option.name}"

class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='orders/%Y/%m/%d/')
    original_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=50)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.original_name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Recharge'),
        ('debit', 'Paiement'),
        ('refund', 'Remboursement'),
        ('bonus', 'Bonus'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('mtn_money', 'MTN Money'),
        ('credits', 'Crédits'),
        ('bank_transfer', 'Virement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, unique=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} FCFA"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order_status', 'Statut commande'),
        ('payment', 'Paiement'),
        ('promotion', 'Promotion'),
        ('system', 'Système'),
        ('maintenance', 'Maintenance'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"