from django.contrib import admin
from catering_employees.models import Employee, Message
from catering_owners.models import CateringCompany, CateringService, CuisineTypeModel, EmployeeWorkService, Event, JobApplication, Menu, Offer, Plate, Review, Task
from catering_particular.models import Particular
from .models import *

# Register your models here.
admin.site.register(CustomUser)