from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from catering_owners.models import JobApplication, NotificationEvent

@receiver(post_save, sender=JobApplication)
def notify_employee_on_state_change(sender, instance, created, **kwargs):
    if not created:  # Verificar si la instancia fue modificada (no creada)
        if instance.state != instance._state.old_state.get('state'):  # Verificar si el campo 'state' ha cambiado
            employee = instance.employee.user
            NotificationEvent.objects.filter(user=employee, has_been_read=True).delete()