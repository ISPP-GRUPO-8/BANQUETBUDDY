from django.urls import path
from core.views import *
from .views import *
from catering_particular.views import *

urlpatterns = [
    path('my_books/<int:event_id>/edit', book_edit, name='book_edit'),
    path('my_books/<int:event_id>/cancel', book_cancel, name='book_cancel'),
    path("caterings/", listar_caterings, name="listar_caterings"),
    path('<int:catering_id>/', catering_detail, name='catering_detail'), 
    path('<int:catering_id>/book/', booking_process, name='booking_process'),
    path('my_books', my_books, name='my_books'),
    path('<int:catering_id>/', catering_detail, name='catering_detail'),
    path('register_particular',register_particular,name='register_particular'),
    path('process/', payment_process, name='process'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_canceled, name='canceled'),
    path('<int:catering_id>/review', catering_review, name='add_review'),
    path('chats/', listar_caterings_companies, name='listar_caterings_companies'),
    path("particular_unsuscribe/", particular_unsuscribe, name="particular_unsuscribe"),
    path('process_premium_particular/', payment_process_premium_particular, name='process_premium_particular'),
    path('completed_premium_particular/', payment_completed_premium_particular, name='completed_premium_particular'),
]
