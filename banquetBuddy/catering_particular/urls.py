from django.urls import path
from . import views
from core.views import *
from catering_particular import views
from .views import booking_process

urlpatterns = [
    path('<int:catering_id>/book/', booking_process, name='booking_process'),
    path('', views.listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', views.catering_detail, name='catering_detail'),
    path('register_particular',views.register_particular,name='register_particular'),
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
