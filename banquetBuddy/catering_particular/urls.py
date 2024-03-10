from django.urls import path
from .views import *

urlpatterns = [
    path('', my_books, name='my_books'),
    path('<int:event_id>/edit', book_edit, name='book_edit'),
    path('<int:event_id>/cancel', book_cancel, name='book_cancel'),
]
