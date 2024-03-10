from django.db import models
from django.contrib.postgres.fields import ArrayField
from catering_particular.models import Particular
from core.models import ApplicationState, AssignmentState, BookingState, CustomUser, PricePlan, Priority
from catering_employees.models import Employee
from phonenumber_field.modelfields import PhoneNumberField

class CateringCompany(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='CateringCompanyusername')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    cif = models.CharField(max_length=20)
    verification_document = models.FileField(upload_to='verification_documents/')
    is_verified = models.BooleanField(default=False)
    service_description = models.TextField(blank=True)
    logo = models.BinaryField(blank=True, null=True)
    cuisine_type = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    price_plan = models.CharField(max_length=50, choices=PricePlan.choices)  

    def __str__(self):
        return self.name
    
class CateringService(models.Model):
    cateringcompany = models.ForeignKey(CateringCompany, on_delete=models.CASCADE, related_name='cateringCompany')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Event(models.Model):
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE, related_name='events')
    particular = models.ForeignKey(Particular, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    details = models.TextField()
    booking_state = models.CharField(max_length=50, choices=BookingState.choices)  
    number_guests = models.IntegerField()

class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE)
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
    cateringservice = models.ForeignKey(CateringService, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plates = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    diet_restrictions = models.CharField(max_length=255)

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

class TaskEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='task_employees')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_employees')