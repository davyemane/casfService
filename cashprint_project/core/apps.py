from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Cash Print - Core'
    
    def ready(self):
        import core.signals  # Importer les signaux