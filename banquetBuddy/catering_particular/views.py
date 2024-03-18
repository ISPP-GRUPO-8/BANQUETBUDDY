from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.contrib import messages
from catering_owners.models import CateringService
from .forms import ParticularForm
from core.forms import CustomUserCreationForm
from catering_owners.models import CateringCompany, CateringService, Menu, Event
from django.contrib import messages
from django.http import HttpResponseForbidden
from core.views import *
from django.db.models import Q
from datetime import datetime
import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

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


def obtener_filtros(request):
    filtros = {
        "cocina": request.GET.get("cocina", ""),
        "precio_maximo": request.GET.get("precio_maximo", ""),
        "num_invitados": request.GET.get("num_invitados", ""),
    }

    limpiar_filtros = {
        "limpiar_cocina": request.GET.get("limpiar_cocina", None),
        "limpiar_precio": request.GET.get("limpiar_precio", None),
        "limpiar_invitados": request.GET.get("limpiar_invitados", None),
    }

    return filtros, limpiar_filtros


def validar_filtros(request, filtros):
    if filtros["precio_maximo"]:
        if not filtros["precio_maximo"].isdigit() or int(filtros["precio_maximo"]) <= 0:
            messages.error(request, "The max price must be a positive number.")
            filtros["precio_maximo"] = ""

    if filtros["num_invitados"]:
        if not filtros["num_invitados"].isdigit() or int(filtros["num_invitados"]) <= 0:
            messages.error(
                request, "The number of attendees must be a positive number."
            )
            filtros["num_invitados"] = ""

    return filtros


def aplicar_filtros(caterings, filtros, limpiar_filtros):
    if filtros["cocina"] and not limpiar_filtros["limpiar_cocina"]:
        caterings = caterings.filter(
            cateringcompany__cuisine_types__type=filtros["cocina"]
        )
    else:
        filtros["cocina"] = ""
    if filtros["precio_maximo"] and not limpiar_filtros["limpiar_precio"]:
        caterings = caterings.filter(price__lte=filtros["precio_maximo"])
    else:
        filtros["precio_maximo"] = ""
    if filtros["num_invitados"] and not limpiar_filtros["limpiar_invitados"]:
        caterings = caterings.filter(capacity__gte=filtros["num_invitados"])
    else:
        filtros["num_invitados"] = ""

    return caterings, filtros


def listar_caterings(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("You are not a particular")
    caterings = CateringService.objects.all()

    # Obtener tipos de cocina únicos
    tipos_cocina = (
        CateringCompany.objects.values_list("cuisine_types__type", flat=True)
        .exclude(cuisine_types__isnull=True)
        .distinct()
    )

    filtros, limpiar_filtros = obtener_filtros(request)
    filtros = validar_filtros(request, filtros)
    caterings, filtros = aplicar_filtros(caterings, filtros, limpiar_filtros)

    context.update(
        {
            "caterings": caterings,
            "tipos_cocina": tipos_cocina,
            **filtros,
        }
    )

    if "search" not in context:
        busqueda = ""

    if request.method == "POST":
        busqueda = request.POST.get("search", "")
        caterings = CateringService.objects.filter(Q(name__icontains=busqueda))

    context["search"] = busqueda
    context["caterings"] = caterings
    return render(request, "listar_caterings.html", context)


def catering_detail(request, catering_id):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)


@login_required
def booking_process(request, catering_id):
    cateringservice = get_object_or_404(CateringService, id=catering_id)
    request.session['catering_service_id'] = cateringservice.id
    catering = get_object_or_404(CateringCompany, user_id = cateringservice.cateringcompany_id)

    eventos = Event.objects.filter(cateringservice_id = catering.user_id)
    highlighted_dates = []
    
    for evento in eventos:
        highlighted_dates.append(evento.date)
    # Obtener el menú para el catering actual
    highlighted_dates_str = [date.strftime('%Y-%m-%d') for date in highlighted_dates]

    

    menus = Menu.objects.filter(cateringcompany_id=catering.user_id)
    
    # Coloca el menú dentro del contexto correctamente
    context = {'cateringservice': cateringservice,'catering': catering, 'menus': menus,'dates' : highlighted_dates_str}
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        request.session['event_date'] = event_date
        number_guests = request.POST.get('number_guests')
        request.session['number_guests'] = number_guests
        selected_menu = request.POST.get('selected_menu')

        # Validación y lógica de reserva aquí
        if not selected_menu:
            messages.error(request, 'Please select a menu')
            context['form_error_menu'] = True
             
        if not (event_date and number_guests and selected_menu):
            messages.error(request, 'Please complete all fields')
            context['form_error'] = True  # Agregar marcador para mostrar mensajes de error

        if int(number_guests) > cateringservice.capacity:
            messages.error(request, 'Number of guests exceeds the catering capacity')
            context['form_error_capacity'] = True

        # Validar que la fecha no esté en el pasado y sea al menos un día en el futuro
        today = datetime.now().date()
        selected_date = datetime.strptime(event_date, '%Y-%m-%d').date()

        if selected_date < today:
            messages.error(request, 'The event date cannot be in the past')
            context['form_error_date'] = True
        elif selected_date == today:
            messages.error(request, 'Reservations must be made at least one day before the event')
            context['form_error_date'] = True

        if Event.objects.filter(cateringservice=cateringservice, date=event_date).exists():
            messages.error(request, 'The selected date is already booked')
            context['form_error_date_selected'] = True

        # Verificar si hay errores en el formulario y, si los hay, volver a renderizar la página con los errores
        if any(key in context for key in ['form_error', 'form_error_capacity', 'form_error_date','form_error_date_selected']):
            return render(request, 'booking_process.html', context)

        # Puedes agregar más lógica según sea necesario

        return payment_process(request, cateringservice.id, selected_menu, number_guests, event_date)

    # Si no es una solicitud POST, renderizar la página con el formulario
    return render(request, 'booking_process.html', context)

def payment_process(request, catering_service_id, selected_menu, number_guests, event_date):
    catering_service = get_object_or_404(CateringService, id=catering_service_id)
    request.session['selected_menu'] = selected_menu
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('completed'))
        cancel_url = request.build_absolute_uri(
            reverse('canceled'))
        # Stripe checkout session data
        session_data = {
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': []
        }
        # add order items to the Stripe checkout session
        session_data['line_items'].append({
            'price_data': {
            'unit_amount': int(catering_service.price * int(number_guests) * Decimal('100')),
            'currency': 'eur',
            'product_data': {
                'name': f"{catering_service.cateringcompany.name} - {catering_service.name} - {number_guests} guests - {selected_menu} - {event_date}",
            },
        },
            'quantity': 1,
        })
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
    
def payment_completed(request):
    menu = Menu.objects.get(id = request.session['selected_menu'])
    catering_service_id = request.session['catering_service_id']
    catering_service = get_object_or_404(CateringService, id = catering_service_id)
        # Crear el evento y hacer la reserva
    event = Event.objects.create(
        cateringservice=catering_service,
        particular= get_object_or_404(Particular, user = request.user),
        name=f'Reservation for {catering_service.cateringcompany.name} by {request.user.username}',
        date=request.session['event_date'],
        details=f'Reservation for {request.session['number_guests']} guests',
        menu = menu,
        booking_state=BookingState.CONTRACT_PENDING,
        number_guests=request.session['number_guests']
    )
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')