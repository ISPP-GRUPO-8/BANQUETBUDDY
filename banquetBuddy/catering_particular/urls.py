from django.urls import path
from core.views import *
from .views import *

urlpatterns = [
    path('', my_books, name='my_books'),
    path('<int:event_id>/edit', book_edit, name='book_edit'),
    path('<int:event_id>/cancel', book_cancel, name='book_cancel'),
    path('<int:catering_id>/book/', booking_process, name='booking_process'),
    path('', listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', catering_detail, name='catering_detail'),
    path('register_particular',register_particular,name='register_particular'),
]
