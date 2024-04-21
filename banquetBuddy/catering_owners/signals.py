from django.db.models.signals import post_save
from django.dispatch import receiver
from catering_owners.models import Event, NotificationEvent

@receiver(post_save, sender=Event)
def notify_employee_on_state_change(sender, instance, created, **kwargs):
    
    if created:
        catering_company_user = instance.cateringservice.cateringcompany.user
        message = f"Your service has been requested for an event on date: {instance.date}."
        NotificationEvent.objects.create(user=catering_company_user, event=instance, message=message)