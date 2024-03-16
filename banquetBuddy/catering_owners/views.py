from django.shortcuts import render, redirect
from .models import CateringCompany
from .forms import CateringCompanyForm
from core.forms import CustomUserCreationForm
from django.contrib import messages
from core.models import *
from django.contrib.auth.decorators import login_required



def register_company(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        company_form = CateringCompanyForm(request.POST, request.FILES)
        
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            company_profile = company_form.save(commit=False)
            company_profile.user = user
            company_profile.save()
            messages.success(request, "Registration successful!")
            # Redirigir al usuario a la página de inicio después del registro exitoso
            return redirect("home")  # Corregido
        else:
            messages.error(request, "Error occurred during registration.")
    else:
        user_form = CustomUserCreationForm()
        company_form = CateringCompanyForm()
    
    return render(
        request,
        "registro_company.html",
        {"user_form": user_form, "company_form": company_form},
    )

@login_required
def catering_profile_edit(request):
    context = {}
    user = request.user

    # Obtener el perfil de la empresa de catering del usuario actual
    catering_company = CateringCompany.objects.get_or_create(user=user)[0]

    if request.method == "POST":
        form = CateringCompanyForm(request.POST, request.FILES, instance=catering_company)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente")
            return redirect("profile")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CateringCompanyForm(instance=catering_company)

    context["form"] = form
    return render(request, "profile_company_edit.html", context)
