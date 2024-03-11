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


