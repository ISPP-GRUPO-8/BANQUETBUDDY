from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from catering_owners.models import JobApplication, NotificationJobApplication

@receiver(post_save, sender=JobApplication)
def notify_employee_on_state_change(sender, instance, **kwargs):
    
    employee = instance.employee.user
    NotificationJobApplication.objects.filter(user=employee, has_been_read=True).delete()
    if instance.state == 'PENDING':
        message = f"Tu aplicación a la oferta {instance.offer.title}, se ha enviado correctamente."
    else:
        message=f"Tu solicitud ha cambiado de estado a {instance.state}."
    NotificationJobApplication.objects.create(user=employee, job_application=instance, message=message)