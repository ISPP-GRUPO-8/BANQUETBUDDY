from django.urls import path
from . import views
from django.urls import path, include
from catering_owners.views import *

urlpatterns = [
    path('applicants/<int:offer_id>/', employee_applications, name='applicants'),
    path('view-reservations/<int:catering_service_id>/',view_reservations,name='view_reservations'),
    path('view-reservations/<int:catering_service_id>/view_reservation/<int:event_id>/',view_reservation,name='view_reservation'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>', catering_calendar_view, name='catering_calendar'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/next_month/', next_month_view, name='next_month'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/prev_month/', prev_month_view, name='prev_month'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/<int:day>/', reservations_for_day, name='reservations_for_day'),
]