from django.urls import path
from . import views
from django.urls import path, include
from core.views import *
from catering_employees import views

urlpatterns = [
    path('', home, name='home'),
    path('register_employee',views.register_employee,name='register_employee'),
    path('applicants/<int:offer_id>/', views.employee_applications, name='applicants'),
    path('employeeOfferList', views.employee_offer_list, name='employeeOfferList'),
    path('employeeApplication/<int:offer_id>/', views.application_to_offer, name='application_to_offer')
]