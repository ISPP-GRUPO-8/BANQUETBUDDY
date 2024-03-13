from django.db import models
from django.contrib.auth.models import User, AbstractUser
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


class Particular(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='ParticularUsername')
    phone_number = PhoneNumberField()
    preferences = models.TextField(blank=True)
    address = models.TextField(blank=True)
    is_subscribed = models.BooleanField(default=False)

class CateringCompany(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='CateringCompanyusername')
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    cuisine_types = models.ManyToManyField('CuisineTypeModel', related_name='catering_companies')
    service_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos_catering/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    price_plan = models.CharField(max_length=50, choices=PricePlan.choices)


class CuisineTypeModel(models.Model):
    type = models.CharField(
        max_length=50,
        choices=CuisineType.choices,
        unique=True
    )

    def __str__(self):
        return self.get_type_display()


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='EmployeeUsername')
    phone_number = PhoneNumberField()
    profession = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    english_level = models.CharField(max_length=50, choices=EnglishLevel.choices, default="NINGUNO")
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

class CateringService(models.Model):
    cateringcompany = models.ForeignKey(CateringCompany, on_delete=models.CASCADE, related_name='cateringCompany')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Event(models.Model):
    cateringservice = models.ForeignKey(CateringService, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    particular = models.ForeignKey(Particular, on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    name = models.CharField(max_length=255)
    date = models.DateField()
    details = models.TextField()
    booking_state = models.CharField(max_length=50, choices=BookingState.choices)  
    number_guests = models.IntegerField()

class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tasks')
    employees = models.ManyToManyField('Employee', related_name='tasks')
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE)
    cateringcompany = models.ForeignKey(CateringCompany, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    assignment_date = models.DateField()
    assignment_state = models.CharField(max_length=50, choices=AssignmentState.choices)  
    expiration_date = models.DateField()
    priority = models.CharField(max_length=50, choices=Priority.choices)  

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(assignment_date__lt=models.F('expiration_date')), name='assignment_before_expiration')
        ]


class Menu(models.Model):
    cateringcompany = models.ForeignKey(CateringCompany, on_delete=models.CASCADE, related_name='menus', null=True, blank=True )
    cateringservice = models.ForeignKey(CateringService, on_delete=models.SET_NULL, null=True, blank=True, related_name='menus')
    name = models.CharField(max_length=255)
    description = models.TextField()
    diet_restrictions = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Plate(models.Model):
    cateringcompany = models.ForeignKey(CateringCompany, on_delete=models.CASCADE, related_name='plates', null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True, related_name='plates')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='plates_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    particular = models.ForeignKey(Particular, on_delete=models.CASCADE, related_name='reviews')
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    description = models.TextField()
    date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name='rating_range')
        ]

class EmployeeWorkService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_work_services')
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE, related_name='employee_work_services')

class Offer(models.Model):
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)

class JobApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='job_applications')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='job_applications')
    date_application = models.DateField()
    state = models.CharField(max_length=50, choices=ApplicationState.choices)  