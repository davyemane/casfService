from django.core.management.base import BaseCommand
from core.models import Service

class Command(BaseCommand):
    help = 'Crée les données initiales nécessaires pour le bon fonctionnement de l\'application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la création même si des services existent déjà',
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Création des données initiales...')
        
        # Vérifier si des services existent déjà
        existing_services = Service.objects.count()
        
        if existing_services > 0 and not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  {existing_services} service(s) existe(nt) déjà. '
                    'Utilisez --force pour recréer.'
                )
            )
            return
        
        if options['force']:
            self.stdout.write('🗑️  Suppression des services existants...')
            Service.objects.all().delete()
        
        # Données des services
        services_data = [
            {
                'name': 'Impression Documents',
                'category': 'impression',
                'description': 'Impression de qualité sur tous formats pour vos communications et documents.',
                'base_price': 25.00,
                'unit': 'page',
                'icon': 'fas fa-file-alt',
                'is_active': True
            },
            {
                'name': 'Badges & Cartes',
                'category': 'badges',
                'description': 'Badges professionnels, cartes de visite et cartes scolaires personnalisées.',
                'base_price': 500.00,
                'unit': 'unité',
                'icon': 'fas fa-id-card',
                'is_active': True
            },
            {
                'name': 'Conception Graphique',
                'category': 'signaletique',
                'description': 'Création d\'affiches publicitaires sur mesure pour vos campagnes.',
                'base_price': 5000.00,
                'unit': 'projet',
                'icon': 'fas fa-palette',
                'is_active': True
            },
            {
                'name': 'Impression Couleur',
                'category': 'impression',
                'description': 'Impression en couleur haute qualité pour tous vos documents.',
                'base_price': 50.00,
                'unit': 'page',
                'icon': 'fas fa-print',
                'is_active': True
            },
            {
                'name': 'Reliure & Finition',
                'category': 'impression',
                'description': 'Services de reliure et de finition pour vos documents professionnels.',
                'base_price': 200.00,
                'unit': 'document',
                'icon': 'fas fa-book',
                'is_active': True
            }
        ]
        
        # Créer les services
        created_count = 0
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Service créé: {service.name} ({service.base_price} FCFA/{service.unit})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Service existant: {service.name}')
                )
        
        # Résumé final
        total_services = Service.objects.filter(is_active=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Terminé! {created_count} service(s) créé(s). '
                f'Total: {total_services} service(s) actif(s).'
            )
        )
        
        if total_services == 0:
            self.stdout.write(
                self.style.ERROR(
                    '❌ ATTENTION: Aucun service actif! '
                    'L\'application ne fonctionnera pas correctement.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ L\'application est prête à fonctionner!'
                )
            )