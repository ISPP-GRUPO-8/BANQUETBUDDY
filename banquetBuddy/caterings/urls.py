from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_caterings, name='listar_caterings'),
]
