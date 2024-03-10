from django.urls import path
from .views import *
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('caterings_contratados', catering_contratados, name='catering_contratados')
]