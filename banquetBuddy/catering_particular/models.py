from django.db import models
from core.models import CustomUser
from catering_employees.models import Message
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


# Create your models here.

class Particular(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='ParticularUsername')
    phone_number = PhoneNumberField()
    preferences = models.TextField(blank=True)
    address = models.TextField(blank=True)
    is_subscribed = models.BooleanField(default=False)

    def send_message(self, receiver, content):
        Message.objects.create(sender=self.user,date=timezone.now(), receiver=receiver, content=content)


    def get_messages(self, other_user):
        return Message.objects.filter(sender=self.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=self.user)
