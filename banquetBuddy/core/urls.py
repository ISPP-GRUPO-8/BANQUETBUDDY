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
    path('profilex-edit', profile_edit_view, name='profile_edit'),
    path('error-report', error_report, name='error-report')    
]
