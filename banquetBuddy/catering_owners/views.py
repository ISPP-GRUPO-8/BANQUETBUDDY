from django.shortcuts import render, redirect, get_object_or_404
from .models import CateringCompany
from .forms import CateringCompanyForm
from core.forms import CustomUserCreationForm
from django.contrib import messages
from core.models import *
from django.contrib.auth.decorators import login_required
from catering_owners.models import *
from datetime import datetime


@login_required
def catering_books(request):
    user = request.user
    catering_company = get_object_or_404(CateringCompany, user=user)
    catering_services = CateringService.objects.filter(cateringcompany_id=catering_company.user_id)
    events = Event.objects.filter(cateringservice__in=catering_services)
    context = {'events': events}
    return render(request, 'particular_books.html', context)

@login_required
def book_catering_cancel(request, event_id):
    user = request.user
    catering_company = get_object_or_404(CateringCompany, user=user)
    catering_service = CateringService.objects.filter(cateringcompany=catering_company)
    event = get_object_or_404(Event, id=event_id)
    
    for service in catering_service:
        if user == service.cateringcompany.user:
            event.booking_state = BookingState.CANCELLED
            event.save()
    
    return redirect("catering_books") 

@login_required
def book_catering_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    catering_company = get_object_or_404(CateringCompany, user=request.user)
    menus = Menu.objects.filter(cateringcompany=catering_company)
    context = {'event': event, 'menus': menus}

    if request.method == "POST":
        date = request.POST.get('date')
        number_guests = request.POST.get('number_guests')
        menu = request.POST.get('selected_menu')

        if number_guests == '0':
            context['error'] = "The number of guests can not be 0."
            return render(request, 'catering_book_edit.html', context)
        
        date2 = datetime.strptime(date, '%Y-%m-%d').date()

        if datetime.now().date() > date2:
            context['error'] = "The selected date cannot be in the past."
            return render(request, 'catering_book_edit.html', context)

        event.date = date
        event.number_guests = number_guests
        event.menu = Menu.objects.get(id=int(menu))
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f'Reservation for {number_guests} guests'
        event.save()

        return redirect("catering_books")

    return render(request, 'catering_book_edit.html', context)


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
