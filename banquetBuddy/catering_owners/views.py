from django.shortcuts import render, redirect, get_object_or_404
from .models import CateringCompany
from .forms import OfferForm,CateringCompanyForm, MenuForm

from core.forms import CustomUserCreationForm
from django.contrib import messages
from core.models import *
from django.contrib.auth.decorators import login_required
from catering_owners.models import *
from datetime import datetime
from .models import CateringCompany, Menu, Plate, Offer, CateringService

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
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
        else:
            messages.error(request, "Plase, correct the errors in the form.")
    else:
        form = CateringCompanyForm(instance=catering_company)

    context["form"] = form
    return render(request, "profile_company_edit.html", context)

###########################
######### Ofertas #########
###########################


@login_required
def offer_list(request):
    
    current_user = request.user
    
    try:
        catering_company = CateringCompany.objects.get(user= current_user)
    except CateringCompany.DoesNotExist:
        return render(request, 'error_catering.html')
    
    offers = Offer.objects.filter(cateringservice__cateringcompany=catering_company)
    return render(request, 'offers/offer_list.html', {'offers': offers})

@login_required
def create_offer(request):
    catering_company = request.user.CateringCompanyusername  
    catering_services = CateringService.objects.filter(cateringcompany=catering_company)
    
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.cateringservice = CateringService.objects.get(pk=request.POST['catering_service'])  # Obtener el CateringService seleccionado en el formulario
            offer.save()
            return redirect('offer_list')
    else:
        form = OfferForm()
    
    return render(request, 'offers/create_offer.html', {'form': form, 'catering_services': catering_services})

@login_required
def edit_offer(request, offer_id): 
    offer = get_object_or_404(Offer, pk=offer_id) 
    if request.user == offer.cateringservice.cateringcompany.user:
        if request.method == 'POST':
            form = OfferForm(request.POST, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('offer_list')  
        else:
            form = OfferForm(instance=offer)
        return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})
    else:
        return redirect('offer_list')

def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offers/delete_offer.html', {'offer': offer})

@login_required
def confirm_delete_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        offer.delete()
        return redirect('offer_list')
    else:
        return redirect('offer_list')
    
def apply_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Procesar la aplicación, por ejemplo, guardarla en la base de datos
            application = form.save(commit=False)
            application.offer = offer  # Asignar la oferta a la aplicación
            application.save()
            # Aquí podrías agregar cualquier lógica adicional, como enviar un correo electrónico de confirmación
            return redirect('offer_list')  # Redirigir de vuelta a la lista de ofertas después de aplicar
    else:
        form = OfferForm()

    return render(request, 'offers/offer_list.html', {'form': form, 'offer': offer})