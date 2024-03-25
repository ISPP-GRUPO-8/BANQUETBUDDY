from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import catering_unsuscribe, create_offer,offer_list,apply_offer,delete_offer,edit_offer, confirm_delete_offer

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
    path('catering_profile_edit', views.catering_profile_edit, name='catering_profile_edit'),
    path('create_offer', create_offer, name='create_offer'),
    path('offer_list', offer_list, name='offer_list'),
    path('apply_offer/<int:offer_id>/', apply_offer, name='apply_offer'),
    path('delete_offer/<int:offer_id>/', delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', edit_offer, name='edit_offer'),
    path('confirm_delete_offer/<int:offer_id>/', confirm_delete_offer, name='confirm_delete_offer'),
    path('catering_unsuscribe/', catering_unsuscribe, name='catering_unsuscribe'),
]

