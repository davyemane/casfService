from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Identifiants incorrects. Veuillez réessayer.')
        return super().form_invalid(form)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Bienvenue sur Cash Print.')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Erreur lors de la création du compte. Vérifiez les informations.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('login')
    
    # Afficher page de confirmation
    return render(request, 'auth/logout_confirm.html')

@login_required
def logout_confirm(request):
    """Vue de confirmation de déconnexion (optionnel)"""
    return render(request, 'auth/logout_confirm.html')