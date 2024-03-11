from django.urls import path

from . import views
from core.views import home
from django.urls import path, include

urlpatterns = [
    path('', home, name='home'),
    path('register_company',views.register_company,name='register_company'),
]