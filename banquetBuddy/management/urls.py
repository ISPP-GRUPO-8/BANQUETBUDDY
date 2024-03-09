from django.urls import path
from . import views
from django.urls import path
from management.views import *

urlpatterns = [
    path('view-reservations/<int:catering_service_id>/',view_reservations,name='view_reservations'),
    path('view-reservations/<int:catering_service_id>/view_reservation/<int:event_id>/',view_reservation,name='view_reservation'),
]
