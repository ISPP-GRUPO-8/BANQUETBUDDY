from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CateringCompanyForm
from core.forms import CustomUserCreationForm
from django.contrib import messages

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
            print(response.content)
            print(response.redirect_chain)
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

