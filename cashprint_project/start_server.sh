#!/bin/bash

# Script de démarrage pour Cash Print avec Gunicorn

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Démarrage du serveur Cash Print...${NC}"

# Vérifier que l'environnement virtuel est activé
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Pensez à activer votre environnement virtuel !${NC}"
fi

# Créer les dossiers nécessaires s'ils n'existent pas
mkdir -p logs
mkdir -p static
mkdir -p media

pip install -r requirements.txt --no-cache-dir
# Migrations Django
echo -e "${YELLOW}📦 Exécution des migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

# Collecte des fichiers statiques
echo -e "${YELLOW}📁 Collecte des fichiers statiques...${NC}"
python manage.py collectstatic --noinput

# Démarrer Gunicorn
echo -e "${GREEN}🔥 Démarrage de Gunicorn...${NC}"
echo -e "${YELLOW}📍 Serveur accessible sur : http://localhost:8000${NC}"
echo -e "${YELLOW}📊 Logs d'accès : logs/access.log${NC}"
echo -e "${YELLOW}🐛 Logs d'erreur : logs/error.log${NC}"
echo ""
echo -e "${GREEN}Appuyez sur Ctrl+C pour arrêter le serveur${NC}"
echo ""

# Lancer Gunicorn avec la configuration
gunicorn -c gunicorn.conf.py cashprint_project.wsgi:application
