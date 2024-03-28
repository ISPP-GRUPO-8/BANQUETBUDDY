from django.apps import AppConfig


class CateringOwnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catering_owners'
    
    def ready(self) -> None:
        from . import signals
