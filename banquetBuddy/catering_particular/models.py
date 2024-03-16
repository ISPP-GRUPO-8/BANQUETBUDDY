from django.db import models
from core.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Particular(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='ParticularUsername')
    phone_number = PhoneNumberField()
    preferences = models.TextField(blank=True)
    address = models.TextField(blank=True)
    is_subscribed = models.BooleanField(default=False)
