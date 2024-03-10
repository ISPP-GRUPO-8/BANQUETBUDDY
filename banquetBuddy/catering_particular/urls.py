from django.urls import path
from . import views
from django.urls import path, include
from core.views import *
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register_particular',register_particular,name='register_particular'),
]