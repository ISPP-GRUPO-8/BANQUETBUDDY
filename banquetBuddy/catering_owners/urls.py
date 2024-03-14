from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from core.views import home
from django.urls import path, include

urlpatterns = [
    path('', home, name='home'),
    path('register_company', views.register_company, name='register_company'),
]

# Configuración para servir archivos estáticos y de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
