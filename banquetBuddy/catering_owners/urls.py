from django.urls import path
from . import views
from django.urls import path, include
from catering_owners.views import *

urlpatterns = [
    path('applicants/<int:offer_id>/', employee_applications, name='applicants'),
]