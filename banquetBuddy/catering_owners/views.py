from django.shortcuts import get_object_or_404, render, redirect
from .forms import CateringCompanyForm, MenuForm
from core.forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Menu, Plate, CateringCompany



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
            messages.success(request, "Menú creado con éxito.")
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
            messages.success(request, "Menú actualizado con éxito.")
            return redirect('list_menus')
    else:
        form = MenuForm(request.user, instance=menu)
    return render(request, 'edit_menu.html', {'form': form})


@login_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=request.user)
    if request.method == 'POST':
        menu.delete()
        messages.success(request, "Menú eliminado con éxito.")
        return redirect('list_menus')
    else:        
        return redirect('list_menus')







