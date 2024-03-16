from django.urls import path
from django.urls import path
from .views import create_offer,offer_list,apply_offer,delete_offer,edit_offer, confirm_delete_offer


urlpatterns = [
    path('create_offer', create_offer, name='create_offer'),
    path('offer_list', offer_list, name='offer_list'),
    path('apply_offer/<int:offer_id>/', apply_offer, name='apply_offer'),
    path('delete_offer/<int:offer_id>/', delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', edit_offer, name='edit_offer'),
    path('confirm_delete_offer/<int:offer_id>/', confirm_delete_offer, name='confirm_delete_offer'),

]