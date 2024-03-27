from django.urls import path
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
    path('register_choice', elegir_registro, name='register_choice'),
    path('profile', profile_view, name='profile'),
    path('profile-edit', profile_edit_view, name='profile_edit'),    
    path('reset_password/', reset_password, name='reset_password'),
    path('reset_password/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
    path('reset_password_complete/', reset_password_complete, name='reset_password_complete'),
    path('profilex-edit', profile_edit_view, name='profile_edit'),
    path('error-report', error_report, name='error-report'),
    path('notifications', notification_view, name='notifications'), 
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', terms_and_conditions, name='terms_and_conditions'),

    
]
