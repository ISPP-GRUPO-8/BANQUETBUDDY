from django.urls import path
from . import views
from django.urls import path
from core.views import *
from catering_employees import views

urlpatterns = [
    path('', home, name='home'),
    path('register_employee',views.register_employee,name='register_employee'),
    path('applicants/<int:offer_id>/', views.employee_applications, name='applicants'),
    path('JobApplicationList', views.employee_applications_list, name='JobApplicationList'),
    path('employeeOfferList', views.employee_offer_list, name='employeeOfferList'),
    path('employeeApplication/<int:offer_id>/', views.application_to_offer, name='application_to_offer'),
    path('<int:employee_id>/recommendation_letters', views.my_recommendation_letters, name='my_recommendation_letters'),
    path('chats/employees', views.listar_caterings_companies, name='listar_caterings_companies_employee'),
]