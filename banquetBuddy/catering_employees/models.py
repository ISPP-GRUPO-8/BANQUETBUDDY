from django.db import models

from core.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='EmployeeUsername')
    phone_number = PhoneNumberField()
    profession = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    curriculum = models.BinaryField(blank=True, null=True)
    recommendation_letter = models.BinaryField(blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_receiver')
    date = models.DateField()
    content = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(sender=models.F('receiver')), name='sender_is_not_receiver')
        ]