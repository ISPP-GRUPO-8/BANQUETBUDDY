from django.apps import AppConfig


class CateringEmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catering_employees'
    
    def ready(self) -> None:
        from . import signals
