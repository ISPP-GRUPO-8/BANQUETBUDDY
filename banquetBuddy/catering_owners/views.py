from django.shortcuts import get_object_or_404, render, redirect
from .forms import CateringCompanyForm, MenuForm
from core.forms import CustomUserCreationForm
from .models import CateringCompany, Menu, Plate
from core.models import *
from django.contrib import messages
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
def list_menus(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    menus = Menu.objects.filter(cateringcompany=catering_company)
    return render(request, 'list_menus.html', {'menus': menus})


@login_required
def add_menu(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    if request.method == 'POST':
        form = MenuForm(request.user, request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.cateringcompany = catering_company
            menu.save()
            messages.success(request, "Menu created successfully..")
            return redirect('list_menus')
    else:
        form = MenuForm(request.user)  

    return render(request, 'add_menu.html', {'form': form})


@login_required
def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=request.user)
    if request.method == 'POST':
        form = MenuForm(request.user, request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu updated successfully.")
            return redirect('list_menus')
    else:
        form = MenuForm(request.user, instance=menu)
    return render(request, 'edit_menu.html', {'form': form})


@login_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=request.user)
    if request.method == 'POST':
        menu.delete()
        messages.success(request, "Menu removed successfully.")
        return redirect('list_menus')
    else:        
        return redirect('list_menus')


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
