from django.urls import path
from django.urls import path
from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('contact', contact, name='contact'),
    path('subscription-plans', subscription_plans, name='subscription_plans'),
    path('faq', faq, name='faq'),
    path('login', login_view, name='login'),
    path('logout/',logout_view, name = 'logout'),
    path('register_choice', elegir_registro, name='register_choice'),
    path('profile', profile_view, name='profile'),
    path('profile-edit', profile_edit_view, name='profile_edit'),    
    path('reset_password/', reset_password, name='reset_password'),
    path('reset_password/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
    path('reset_password_complete/', reset_password_complete, name='reset_password_complete'),


]
