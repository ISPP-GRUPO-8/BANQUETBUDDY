from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from core.views import home
from django.urls import path, include



urlpatterns = [
    path('', home, name='home'),
    path('register_company', views.register_company, name='register_company'),
    path('list_menus/', views.list_menus, name='list_menus'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('edit_menu/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('delete_menu/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('catering_profile_edit', views.catering_profile_edit, name='catering_profile_edit')
]

# Configuración para servir archivos estáticos y de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

