from django.shortcuts import render, redirect
from django.contrib import messages

from catering_owners.models import CateringService
from .forms import ParticularForm
from core.forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from core.views import *
from django.db.models import Q

# Create your views here.

def register_particular(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        particular_form = ParticularForm(request.POST)

        if user_form.is_valid() and particular_form.is_valid():

            user = user_form.save()

            particular_profile = particular_form.save(commit=False)
            particular_profile.user = user
            particular_profile.save()
            messages.success(request, "Registration successful!")

            return redirect("home")

    else:
        user_form = CustomUserCreationForm()
        particular_form = ParticularForm()

    return render(
        request,
        "core/registro_particular.html",
        {"user_form": user_form, "particular_form": particular_form},
    )


def listar_caterings(request):
    context = {}
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    caterings = CateringService.objects.all()
    if 'buscar' not in context:
        busqueda = ''

    if request.method == 'POST':
        busqueda = request.POST.get('buscar', '')
        caterings = CateringService.objects.filter(Q(name__icontains=busqueda))
        
    context['buscar'] = busqueda    
    context['caterings'] = caterings
    return render(request, 'listar_caterings.html', context)


def catering_detail(request, catering_id):
    context = {}
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)
