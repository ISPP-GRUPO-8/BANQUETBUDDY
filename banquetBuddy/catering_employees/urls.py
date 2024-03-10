from django.urls import path
from . import views
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('register_employee',views.register_employee,name='register_employee'),
]