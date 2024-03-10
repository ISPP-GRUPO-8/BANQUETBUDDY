from django.urls import path
from .views import *

urlpatterns = [
    path('', listar_caterings, name='listar_caterings'),
    path('<int:catering_id>/', catering_detail, name='catering_detail'), 
    path('<int:catering_id>/review', catering_review, name='add_review'), 

]
