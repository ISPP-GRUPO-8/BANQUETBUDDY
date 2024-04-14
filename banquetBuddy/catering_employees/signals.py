from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from catering_owners.models import JobApplication, NotificationJobApplication

@receiver(post_save, sender=JobApplication)
def notify_employee_on_state_change(sender, instance, **kwargs):
    
    employee = instance.employee.user
    message = f"Your application to {instance.offer.title}, has been sent correctly."
    title = str(instance.offer.title)
    NotificationJobApplication.objects.create(user=employee, job_application=instance, message=message, title=title)