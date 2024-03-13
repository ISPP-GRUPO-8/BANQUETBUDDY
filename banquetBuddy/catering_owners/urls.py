from django.urls import path
from . import views
from django.urls import path, include
from catering_owners.views import *

urlpatterns = [
    path('applicants/<int:offer_id>/', employee_applications, name='applicants'),
    path('view-reservations/<int:catering_service_id>/',view_reservations,name='view_reservations'),
    path('view-reservations/<int:catering_service_id>/view_reservation/<int:event_id>/',view_reservation,name='view_reservation'),
]