from django.urls import path

from core.views import home
from . import views
from django.urls import path, include
from catering_owners.views import employee_applications

urlpatterns = [
    path('', home, name='home'),
    path('register_company',views.register_company,name='register_company'),
]