#!/bin/bash

# Script de déploiement sécurisé pour CashPrint
# Ce script garantit que l'application fonctionne après déploiement

echo "🚀 Déploiement CashPrint..."

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. Migrations de base de données
echo "📊 Application des migrations..."
python manage.py makemigrations
python manage.py migrate

if [ $? -eq 0 ]; then
    print_status "Migrations appliquées avec succès"
else
    print_error "Erreur lors des migrations"
    exit 1
fi

# 2. Collecte des fichiers statiques (pour production)
if [ "$1" = "production" ]; then
    echo "📁 Collecte des fichiers statiques..."
    python manage.py collectstatic --noinput
    print_status "Fichiers statiques collectés"
fi

# 3. Vérification des services existants
echo "🔍 Vérification des services..."
SERVICE_COUNT=$(python manage.py shell -c "from core.models import Service; print(Service.objects.filter(is_active=True).count())")

if [ "$SERVICE_COUNT" = "0" ]; then
    print_warning "Aucun service trouvé, création des données initiales..."
    
    # Créer les données initiales
    python manage.py create_initial_data
    
    if [ $? -eq 0 ]; then
        print_status "Données initiales créées avec succès"
    else
        print_error "Erreur lors de la création des données initiales"
        exit 1
    fi
else
    print_status "$SERVICE_COUNT service(s) actif(s) trouvé(s)"
fi

# 4. Création d'un superuser si nécessaire (uniquement en développement)
if [ "$1" != "production" ]; then
    echo "👤 Vérification du superuser..."
    SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())")
    
    if [ "$SUPERUSER_EXISTS" = "False" ]; then
        print_warning "Aucun superuser trouvé"
        echo "Voulez-vous créer un superuser? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            python manage.py createsuperuser
        fi
    else
        print_status "Superuser existant trouvé"
    fi
fi

# 5. Test de santé de l'application
echo "🏥 Test de santé de l'application..."

# Vérifier que les modèles sont accessibles
python manage.py shell -c "
from core.models import Service, UserProfile, Order
services = Service.objects.filter(is_active=True).count()
print(f'Services actifs: {services}')
if services == 0:
    print('ERREUR: Aucun service actif!')
    exit(1)
else:
    print('✅ Application prête!')
"

if [ $? -eq 0 ]; then
    print_status "Test de santé réussi"
else
    print_error "Test de santé échoué"
    exit 1
fi

# 6. Instructions finales
echo ""
echo "🎉 Déploiement terminé avec succès!"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Démarrer le serveur: python manage.py runserver"
echo "   2. Accéder à l'application: http://127.0.0.1:8000/"
echo "   3. Tester la création de commande: http://127.0.0.1:8000/orders/new/"
if [ "$1" != "production" ]; then
    echo "   4. Admin Django: http://127.0.0.1:8000/admin/"
fi
echo ""
print_status "Application prête pour utilisation!"