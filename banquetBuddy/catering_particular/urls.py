from django.urls import path, include
from . import views
from core.views import *
from .views import *
from . import views
from catering_particular.views import *

urlpatterns = [
    # path('my_books', my_books, name='my_books'),
    # path('my_books/<int:event_id>/edit', book_edit, name='book_edit'),
    # path('my_books/<int:event_id>/cancel', book_cancel, name='book_cancel'),
    path('', listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', catering_detail, name='catering_detail'), 
    path('<int:catering_id>/book/', booking_process, name='booking_process'),
    path('caterings_contratados', catering_contratados, name='catering_contratados'),
    path('', listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', catering_detail, name='catering_detail'),
    path('register_particular',register_particular,name='register_particular'),
    path('process/', payment_process, name='process'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_canceled, name='canceled'),
    path('<int:catering_id>/review', catering_review, name='add_review'),
]
