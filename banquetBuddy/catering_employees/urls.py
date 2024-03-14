from django.urls import path
from . import views
from django.urls import path, include
from core.views import *
from catering_employees import views

urlpatterns = [
    path('', home, name='home'),
    path('register_employee',views.register_employee,name='register_employee'),
    path('applicants/<int:offer_id>/', views.employee_applications, name='applicants'),
]