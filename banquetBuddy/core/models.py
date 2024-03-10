from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User, AbstractUser
from enum import Enum
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class AssignmentState(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'

class PricePlan(models.TextChoices):
    BASE = 'BASE', 'Base'
    PREMIUM = 'PREMIUM', 'Premium'
    PREMIUM_PRO = 'PREMIUM_PRO', 'Premium Pro'
    NO_SUBSCRIBED = 'NO_SUBSCRIBED', 'No Subscribed'

class ApplicationState(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_REVIEW = 'IN_REVIEW', 'In Review'
    ACCEPTED = 'ACCEPTED', 'Accepted'

class Priority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

class BookingState(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CONTRACT_PENDING = 'CONTRACT_PENDING', 'Contract Pending'
    CANCELLED = 'CANCELLED', 'Cancelled'



