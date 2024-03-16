from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from core.views import home
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register_company', views.register_company, name='register_company'),
    path('catering_profile_edit', views.catering_profile_edit, name='catering_profile_edit'),
    path('catering_books', catering_books, name='catering_books'),
    path('catering_books/<int:event_id>/edit', book_catering_edit, name='catering_books_edit'),
    path('catering_books/<int:event_id>/cancel', book_catering_cancel, name='catering_books_cancel'),
]

# Configuración para servir archivos estáticos y de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

