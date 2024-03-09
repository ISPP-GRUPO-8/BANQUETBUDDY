from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from core.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def employee_applications(request, offer_id):
    
    offer = Offer.objects.get(pk=offer_id)
    applicants = offer.job_applications.select_related('employee').all()
    
    context = {'applicants': applicants, 'offer': offer}
    return render(request, "applicants_list.html", context)
