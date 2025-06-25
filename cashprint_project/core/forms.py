from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Order, Service, ServiceOption

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES, required=True)
    phone = forms.CharField(max_length=20, required=False)
    institution = forms.CharField(max_length=200, required=False)
    student_id = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'user_type': self.cleaned_data['user_type'],
                    'phone': self.cleaned_data['phone'],
                    'institution': self.cleaned_data['institution'],
                    'student_id': self.cleaned_data['student_id']
                }
            )
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'institution', 'student_id', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'institution': forms.TextInput(attrs={'class': 'form-input'}),
            'student_id': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

class CreditRechargeForm(forms.Form):
    PAYMENT_METHODS = [
        ('orange_money', 'Orange Money'),
        ('mtn_money', 'MTN Money'),
        ('bank_transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
    ]
    
    amount = forms.DecimalField(
        min_value=1000, 
        max_value=500000, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Montant en FCFA'})
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service', 'quantity', 'special_instructions']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'base_price', 'unit', 'is_active', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ServiceOptionForm(forms.ModelForm):
    class Meta:
        model = ServiceOption
        fields = ['name', 'option_group', 'description', 'price', 'is_required', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'option_group': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }