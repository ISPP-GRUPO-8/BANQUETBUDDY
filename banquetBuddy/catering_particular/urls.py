from django.urls import path
from . import views
from core.views import *
from catering_particular import views

urlpatterns = [
    path('', views.listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', views.catering_detail, name='catering_detail'),
    path('register_particular',views.register_particular,name='register_particular'),
]
