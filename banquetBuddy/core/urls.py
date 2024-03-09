from django.urls import path
from . import views
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('contact', contact, name='contact'),
    path('subscription-plans', subscription_plans, name='subscription_plans'),
    path('faq', faq, name='faq'),
    path('login', login_view, name='login'),
    path('logout/',logout_view, name = 'logout'),
    path('register_particular',register_particular,name='register_particular'),
    path('register_employee',register_employee,name='register_employee'),
    path('register_company',register_company,name='register_company'),
    path('register_choice', elegir_registro, name='register_choice'),
    path('profile', profile_view, name='profile'),
    path('profile-edit', profile_edit_view, name='profile_edit'),
    path('create_offer', create_offer, name='create_offer'),
    path('offer_list', offer_list, name='offer_list'),
    path('apply_offer/<int:offer_id>/', views.apply_offer, name='apply_offer'),
    path('delete_offer/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),

    


]
