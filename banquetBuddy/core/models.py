from django.db import models
from django.contrib.auth.models import User, AbstractUser
from banquetBuddy import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)

    def generate_reset_password_token(self):
        token = get_random_string(length=32)

        # Asignar el token al usuario
        self.reset_password_token = token
        self.save()


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
    REJECTED = 'REJECTED', 'Rejected'
    ACCEPTED = 'ACCEPTED', 'Accepted'

class Priority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

class BookingState(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CONTRACT_PENDING = 'CONTRACT_PENDING', 'Contract Pending'
    CANCELLED = 'CANCELLED', 'Cancelled'
    FINALIZED = 'FINALIZED', 'Finalized'

class EnglishLevel(models.TextChoices):
    C2 = 'C2', 'C2'
    C1 = 'C1', 'C1'
    B2 = 'B2', 'B2'
    B1 = 'B1', 'B1'
    A2 = 'A2', 'A2'
    A1 = 'A1', 'A1'
    NINGUNO = 'NONE', 'None'

class CuisineType(models.TextChoices):
    MEDITERRANEAN = 'MEDITERRANEAN', 'Mediterránea'
    ORIENTAL = 'ORIENTAL', 'Oriental'
    MEXICAN = 'MEXICAN', 'Mexicana'
    ITALIAN = 'ITALIAN', 'Italiana'
    FRENCH = 'FRENCH', 'Francesa'
    SPANISH = 'SPANISH', 'Española'
    INDIAN = 'INDIAN', 'India'
    CHINESE = 'CHINESE', 'China'
    JAPANESE = 'JAPANESE', 'Japonesa'
    THAI = 'THAI', 'Tailandesa'
    GREEK = 'GREEK', 'Griega'
    LEBANESE = 'LEBANESE', 'Libanesa'
    TURKISH = 'TURKISH', 'Turca'
    KOREAN = 'KOREAN', 'Coreana'
    VIETNAMESE = 'VIETNAMESE', 'Vietnamita'
    AMERICAN = 'AMERICAN', 'Americana'
    BRAZILIAN = 'BRAZILIAN', 'Brasileña'
    ARGENTINE = 'ARGENTINE', 'Argentina'
    VEGETARIAN = 'VEGETARIAN', 'Vegetariana'
    VEGAN = 'VEGAN', 'Vegana'
    GLUTEN_FREE = 'GLUTEN_FREE', 'Sin Gluten'
    SEAFOOD = 'SEAFOOD', 'Mariscos'
    BBQ = 'BBQ', 'Barbacoa'
    FAST_FOOD = 'FAST_FOOD', 'Comida Rápida'
    FUSION = 'FUSION', 'Fusión'
    TRADITIONAL = 'TRADITIONAL', 'Tradicional'
    ORGANIC = 'ORGANIC', 'Orgánica'
    GOURMET = 'GOURMET', 'Gourmet'


