from core.models import *
import re
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from core.models import BookingState
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from core.forms import CustomUserCreationForm
from catering_owners.models import *
from .forms import ParticularForm
from django.http import HttpResponseForbidden
from core.views import *
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def my_books(request):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    return render(request, 'my_books.html', context)

@login_required
def book_cancel(request, event_id):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    event = get_object_or_404(Event, id = event_id)
    if user.id == event.particular_id:
        event.booking_state = BookingState.CANCELLED
        event.save()
    return render(request, 'my_books.html', context)

@login_required
def book_edit(request, event_id):
    context = {}
    event = get_object_or_404(Event, id = event_id)
    events = Event.objects.filter(particular_id = request.user.id)
    catering_service = get_object_or_404(CateringService, id = event.cateringservice_id)
    catering = get_object_or_404(CateringCompany, user_id = catering_service.cateringcompany_id)
    menus = Menu.objects.filter(cateringcompany_id = catering.user_id)
    context["menus"] = menus
    context["event"] = event

    if request.method == "POST":
        date = request.POST.get('date')
        number_guests = request.POST.get('number_guests')
        menu = request.POST.get('selected_menu')

        context["date"] = date
        context["number_guests"] = number_guests
        context["menu"] = menu
        context["events"] = events

        if number_guests == '0':
            context['error'] = "The number of guests can not be 0."
            return render(request, 'book_edit.html', context)
        
        date2 = datetime.strptime(date, '%Y-%m-%d').date()

        if datetime.now().date() > date2:
            context['error'] = "The selected date cannot be in the past."
            return render(request, 'book_edit.html', context)

        event.date = date
        event.number_guests = number_guests
        event.menu = Menu.objects.get(id = menu)
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f'Reservation for {number_guests} guests'
        event.save()

        return render(request, 'my_books.html', context)

    return render(request, 'book_edit.html', context)

# Create your views here.

@login_required
def my_books(request):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    return render(request, 'my_books.html', context)

@login_required
def book_cancel(request, event_id):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    event = get_object_or_404(Event, id = event_id)
    if user.id == event.particular_id:
        event.booking_state = BookingState.CANCELLED
        event.save()
    return render(request, 'my_books.html', context)

@login_required
def book_edit(request, event_id):
    context = {}
    event = get_object_or_404(Event, id = event_id)
    events = Event.objects.filter(particular_id = request.user.id)
    catering = get_object_or_404(CateringService, id = event.cateringservice_id)
    menus = Menu.objects.filter(cateringservice_id = catering.id)
    context["menus"] = menus
    context["event"] = event

    if request.method == "POST":
        date = request.POST.get("date", "")
        number_guests = request.POST.get("number_guests", "")
        menu = request.POST.get("menu", "")

        context["date"] = date
        context["number_guests"] = number_guests
        context["menu"] = menu
        context["events"] = events

        event.date = date
        event.number_guests = number_guests
        event.menu = menu
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f'Reservation for {number_guests} guests'
        event.save()

        return render(request, 'my_books.html', context)

    return render(request, 'book_edit.html', context)


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
        "ciudad": request.GET.get("ciudad", ""),
    }

    limpiar_filtros = {
        "limpiar_cocina": request.GET.get("limpiar_cocina", None),
        "limpiar_precio": request.GET.get("limpiar_precio", None),
        "limpiar_invitados": request.GET.get("limpiar_invitados", None),
        "limpiar_ciudad": request.GET.get("limpiar_ciudad", None),
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
    if filtros["ciudad"] and not limpiar_filtros["limpiar_ciudad"]:
        caterings = caterings.filter(Q(location__icontains=filtros["ciudad"]))
    else:
        filtros["ciudad"] = ""

    return caterings, filtros


def listar_caterings(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("You are not a particular")
    caterings = CateringService.objects.all()

    for catering in caterings:
        print(catering.location)

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
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    
    reviews_list = Review.objects.filter(cateringservice_id=catering_id).order_by('-date')
    
    paginator = Paginator(reviews_list, 3)  # Muestra 3 reviews por página
    page = request.GET.get('page')

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    context['reviews'] = reviews
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id=catering_id)
    context["catering"] = catering
    return render(request, "catering_detail.html", context)

def catering_review(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)
    user = request.user
    particular = Particular.objects.filter(user_id=user.id)

    if particular:
        context = {'catering': catering, 'particular':particular}

        if request.method == 'POST':
            description = request.POST.get('description')
            rating = request.POST.get('rating')

            review = Review.objects.create(
                cateringservice=catering,
                particular=Particular.objects.get(user=user),
                date=datetime.now().date(),
                description=description,
                rating=rating
            )

            url_catering = reverse('catering_detail', args=[catering.id])
            return redirect(url_catering)
    else:
        return redirect("/")

    return render(request, 'catering_review.html', context)


@login_required
def booking_process(request, catering_id):
    cateringservice = get_object_or_404(CateringService, id=catering_id)
    catering = get_object_or_404(
        CateringCompany, user_id=cateringservice.cateringcompany_id
    )
    user = request.user
    particular = get_object_or_404(Particular, user_id=user.id)

    eventos = Event.objects.filter(cateringservice_id=catering.user_id)
    highlighted_dates = []

    for evento in eventos:
        highlighted_dates.append(evento.date)
    # Obtener el menú para el catering actual
    highlighted_dates_str = [date.strftime("%Y-%m-%d") for date in highlighted_dates]

    menus = Menu.objects.filter(cateringcompany_id=catering.user_id)

    # Coloca el menú dentro del contexto correctamente
    context = {
        "cateringservice": cateringservice,
        "catering": catering,
        "menus": menus,
        "dates": highlighted_dates_str,
    }
    if request.method == "POST":
        event_date = request.POST.get("event_date")
        number_guests = request.POST.get("number_guests")
        selected_menu = request.POST.get("selected_menu")

        # Validación y lógica de reserva aquí
        if not selected_menu:
            messages.error(request, "Please select a menu")
            context["form_error_menu"] = True

        if not (event_date and number_guests and selected_menu):
            messages.error(request, "Please complete all fields")
            context["form_error"] = (
                True  # Agregar marcador para mostrar mensajes de error
            )

        if int(number_guests) > cateringservice.capacity:
            messages.error(request, "Number of guests exceeds the catering capacity")
            context["form_error_capacity"] = True

        # Validar que la fecha no esté en el pasado y sea al menos un día en el futuro
        today = datetime.now().date()
        selected_date = datetime.strptime(event_date, "%Y-%m-%d").date()

        if selected_date < today:
            messages.error(request, "The event date cannot be in the past")
            context["form_error_date"] = True
        elif selected_date == today:
            messages.error(
                request, "Reservations must be made at least one day before the event"
            )
            context["form_error_date"] = True

        if Event.objects.filter(
            cateringservice=cateringservice, date=event_date
        ).exists():
            messages.error(request, "The selected date is already booked")
            context["form_error_date_selected"] = True

        # Verificar si hay errores en el formulario y, si los hay, volver a renderizar la página con los errores
        if any(
            key in context
            for key in [
                "form_error",
                "form_error_capacity",
                "form_error_date",
                "form_error_date_selected",
            ]
        ):
            return render(request, "booking_process.html", context)

        menu = Menu.objects.get(id=selected_menu)
        # Crear el evento y hacer la reserva
        event = Event.objects.create(
            cateringservice=cateringservice,
            particular=particular,
            name=f"Reservation for {catering.name} by {user.username}",
            date=event_date,
            details=f"Reservation for {number_guests} guests",
            menu=menu,
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=number_guests,
        )

        # Puedes agregar más lógica según sea necesario

        return redirect("/")

    # Si no es una solicitud POST, renderizar la página con el formulario
    return render(request, "booking_process.html", context)