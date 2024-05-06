from django.shortcuts import render, get_object_or_404, redirect, reverse
from core.models import BookingState
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from core.forms import CustomUserCreationForm
from catering_owners.models import *
from .forms import ParticularForm
from django.http import HttpResponseForbidden
from core.views import *
from django.contrib.auth.decorators import login_required
from core.models import *
from django.db.models import Q
from datetime import datetime
import stripe
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from core.permission_checks import is_user_particular
import random


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
from django.core.paginator import Paginator

NOT_PARTICULAR_ERROR = "You are not registered as a particular"
FORBIDDEN_ACCESS_ERROR = "You are not allowed to access to the following page"


@login_required
def my_books(request):
    user = request.user
    events_list = Event.objects.filter(particular_id=user.id).order_by('-date')

    paginator = Paginator(events_list, 3)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    context = {
        "events": events,
    }
    return render(request, "my_books.html", context)



@login_required
def book_cancel(request, event_id):
    user = request.user
    events = Event.objects.filter(particular_id=user.id)
    context = {"events": events}
    event = get_object_or_404(Event, id=event_id)
    if user.id == event.particular_id:
        event.booking_state = BookingState.CANCELLED
        event.save()
    return redirect('my_books')


@login_required
def book_edit(request, event_id):
    context = {}
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.filter(particular_id=request.user.id)
    catering_service = get_object_or_404(CateringService, id=event.cateringservice_id)
    catering = get_object_or_404(
        CateringCompany, user_id=catering_service.cateringcompany_id
    )
    menus = Menu.objects.filter(cateringcompany_id=catering.user_id)
    context["menus"] = menus
    context["event"] = event

    if request.method == "POST":
        date = request.POST.get("date")
        number_guests = request.POST.get("number_guests")
        menu = request.POST.get("selected_menu")

        context["date"] = date
        context["number_guests"] = number_guests
        context["menu"] = menu
        context["events"] = events

        if number_guests == "0":
            context["error"] = "The number of guests can not be 0"
            return render(request, "book_edit.html", context)

        date2 = datetime.strptime(date, "%Y-%m-%d").date()

        if datetime.now().date() > date2:
            context["error"] = "The selected date cannot be in the past"
            return render(request, "book_edit.html", context)
        
        if datetime.now().date() == date2:
            context["error"] = "Reservations must be made at least one day before the event"
            return render(request, "book_edit.html", context)
        
        if not menu:
            context["error"] = "Please select a menu"
            return render(request, "book_edit.html", context)

        if not (date and number_guests and menu):
            context["error"] = "Please complete all fields"
            return render(request, "book_edit.html", context)
            
        if int(number_guests) > catering_service.capacity:
            context["error"] = "Number of guests exceeds the catering capacity"
            return render(request, "book_edit.html", context)
            
        event.date = date
        event.number_guests = number_guests
        event.menu = Menu.objects.get(id=menu)
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f"Reservation for {number_guests} guests"
        event.save()

        return redirect('my_books')

    return render(request, "book_edit.html", context)


# Create your views here.


def register_particular(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        particular_form = ParticularForm(request.POST)

        if user_form.is_valid() and particular_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = (
                False  # Desactiva la cuenta hasta que se confirme el correo electrónico
            )
            user.save()

            particular_profile = particular_form.save(commit=False)
            particular_profile.user = user
            particular_profile.save()

            # Genera un token único para el usuario
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Obtiene el dominio actual
            domain = get_current_site(request).domain
            # Crea el enlace de confirmación
            link = f"http://{domain}/activate/{uid}/{token}/particular"
            # Renderiza el correo electrónico
            mail_subject = "Activate your account"
            message = render_to_string(
                "core/activation_email.html",
                {
                    "user": user,
                    "domain": domain,
                    "uid": uid,
                    "token": token,
                },
            )
            # Envia el correo electrónico
            send_mail(
                mail_subject, message, "banquetbuddyoficial@gmail.com", [user.email]
            )

            messages.success(
                request,
                "Registration successful! Please confirm your email address to complete the registration",
            )

            return redirect("home")

    else:
        user_form = CustomUserCreationForm()
        particular_form = ParticularForm()

    return render(
        request,
        "core/registro_particular.html",
        {"user_form": user_form, "particular_form": particular_form},
    )


@login_required
def catering_contratados(request):
    current_user = request.user
    context = {}
    if not is_user_particular(current_user):
        return HttpResponseForbidden(NOT_PARTICULAR_ERROR)
    particular = get_object_or_404(Particular, user=current_user)
    events = Event.objects.filter(particular=particular)
    context["events"] = events
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    return render(request, "catering_contratado.html", context)


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
        return HttpResponseForbidden(NOT_PARTICULAR_ERROR)
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

    reviews_list = Review.objects.filter(cateringservice_id=catering_id).order_by(
        "-date"
    )
    
    # Paginación
    paginator = Paginator(reviews_list, 3)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    context["reviews"] = reviews
    if not is_particular(request):
        return HttpResponseForbidden(NOT_PARTICULAR_ERROR)
    catering = get_object_or_404(CateringService, id=catering_id)
    context["catering"] = catering
    return render(request, "catering_detail.html", context)


@login_required
def catering_review(request, catering_id):
    user = request.user
    catering = get_object_or_404(CateringService, id=catering_id)
    if not is_user_particular(user):
        return HttpResponseForbidden(NOT_PARTICULAR_ERROR)
    
    has_been_booked = False
    particular = Particular.objects.filter(user_id=user.id)
    particular_events = Event.objects.filter(particular=particular[0], cateringservice=catering)
    
    for event in particular_events:
        if event.date <= timezone.now().date():
            has_been_booked = True
            break
        else:
            messages.error(request, "You cannot leave a review until after the event date has passed.")
            return redirect("listar_caterings")

    if not has_been_booked:
        messages.error(request, "You must have attended an event with this catering service before reviewing it.")
        return redirect("listar_caterings")

    if particular:
        context = {"catering": catering, "particular": particular}

        if request.method == "POST":
            description = request.POST.get("description")
            rating = request.POST.get("rating")

            review = Review.objects.create(
                cateringservice=catering,
                particular=Particular.objects.get(user=user),
                date=datetime.now().date(),
                description=description,
                rating=rating,
            )

            url_catering = reverse("catering_detail", args=[catering.id])
            return redirect(url_catering)
    else:
        return redirect("/")

    return render(request, "catering_review.html", context)


@login_required
def booking_process(request, catering_id):
    cateringservice = get_object_or_404(CateringService, id=catering_id)
    request.session["catering_service_id"] = cateringservice.id
    catering = get_object_or_404(
        CateringCompany, user_id=cateringservice.cateringcompany_id
    )
    user = request.user
    if not is_particular(request):
        return HttpResponseForbidden(NOT_PARTICULAR_ERROR)

    eventos = Event.objects.filter(cateringservice_id=catering.user_id)
    highlighted_dates = []

    for evento in eventos:
        highlighted_dates.append(evento.date)
    # Obtener el menú para el catering actual
    highlighted_dates_str = [date.strftime("%Y-%m-%d") for date in highlighted_dates]

    menus = Menu.objects.filter(cateringservice=cateringservice.id)

    menus_plates = {}
    for m in menus:
        plates = Plate.objects.filter(menu=m)
        menus_plates[m] = plates        

    # Coloca el menú dentro del contexto correctamente
    context = {
        "cateringservice": cateringservice,
        "catering": catering,
        "menus": menus,
        "menus_with_plates": menus_plates,
        "dates": highlighted_dates_str,
    }

    if request.method == "POST":
        event_date = request.POST.get("event_date")
        request.session["event_date"] = event_date
        number_guests = request.POST.get("number_guests")
        request.session["number_guests"] = number_guests
        selected_menu = request.POST.get("selected_menu")

        # Validación y lógica de reserva aquí
        if number_guests == "0":
            context["form_error_guests"] = True
        
        if not selected_menu:
            context["form_error_menu"] = True

        if not (event_date and number_guests and selected_menu):
            context["form_error"] = (
                True  # Agregar marcador para mostrar mensajes de error
            )

        if int(number_guests) > cateringservice.capacity:
            context["form_error_capacity"] = True

        # Validar que la fecha no esté en el pasado y sea al menos un día en el futuro
        today = datetime.now().date()
        selected_date = datetime.strptime(event_date, "%Y-%m-%d").date()

        if selected_date < today:
            context["form_error_date"] = True
        elif selected_date == today:
            context["form_error_date"] = True

        if Event.objects.filter(
            cateringservice=cateringservice, date=event_date
        ).exists():
            context["form_error_date_selected"] = True

        # Verificar si hay errores en el formulario y, si los hay, volver a renderizar la página con los errores

        form_errors = {
            "form_error",
                "form_error_guests",
                "form_error_menu",
                "form_error_capacity",
                "form_error_date",
                "form_error_date_selected",
        }
        if any(key in context for key in form_errors):

            return render(request, "booking_process.html", context)

        # Puedes agregar más lógica según sea necesario

        return payment_process(
            request, cateringservice.id, selected_menu, number_guests, event_date
        )

    # Si no es una solicitud POST, renderizar la página con el formulario
    return render(request, "booking_process.html", context)



@login_required
def payment_process(
    request, catering_service_id, selected_menu, number_guests, event_date
):
    catering_service = get_object_or_404(CateringService, id=catering_service_id)
    request.session["selected_menu"] = selected_menu
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("completed"))
        cancel_url = request.build_absolute_uri(reverse("canceled"))
        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        price_to_pay= catering_service.price * int(number_guests) * Decimal("100")
        if(request.user.ParticularUsername.is_subscribed == True):
            price_to_pay = price_to_pay*Decimal(0.95)
        
        # add order items to the Stripe checkout session
        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(price_to_pay),
                    "currency": "eur",
                    "product_data": {
                        "name": f"{catering_service.cateringcompany.name} - {catering_service.name} - {number_guests} guests - {selected_menu} - {event_date}",
                    },
                },
                "quantity": 1,
            }
        )
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    menu = Menu.objects.get(id=request.session["selected_menu"])
    catering_service_id = request.session["catering_service_id"]
    catering_service = get_object_or_404(CateringService, id=catering_service_id)

    # Asignar la empresa de catering vinculada al servicio de catering
    catering_company = catering_service.cateringcompany
    random_number = random.randint(1, 999)
    # Crear el evento y hacer la reserva
    event = Event.objects.create(
        cateringservice=catering_service,
        cateringcompany=catering_company,  # Asignar la empresa de catering
        particular=get_object_or_404(Particular, user=request.user),
        name=f"Reservation for {catering_service.cateringcompany.name} by {request.user.username} #{random_number}",
        date=request.session["event_date"],
        details=f'Reservation for {request.session["number_guests"]} guests',
        menu=menu,
        booking_state=BookingState.CONFIRMED,
        number_guests=request.session["number_guests"],
    )
    return render(request, "payment/completed.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")


def listar_caterings_companies(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    caterings = CateringCompany.objects.all()
    if "search" not in context:
       busqueda = ""

    if request.method == "POST":
        busqueda = request.POST.get("search", "")
        caterings = CateringCompany.objects.filter(Q(name__icontains=busqueda))
    

    context["caterings"] = caterings
    return render(request, "contact_chat.html", context)

@login_required
def particular_unsuscribe(request):
    particular = Particular.objects.get(user=request.user)
    print(particular.is_subscribed)
    particular.is_subscribed = False
    particular.save()
    print(particular.is_subscribed)
    return redirect("profile")

@login_required
def payment_process_premium_particular(request):
        success_url = request.build_absolute_uri(reverse("completed_premium_particular"))
        cancel_url = request.build_absolute_uri(reverse("canceled"))
        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        # add order items to the Stripe checkout session
        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(
                        499
                    ),
                    "currency": "eur",
                    "product_data": {
                        "name": f"PREMIUM PLAN SUBSCRIPTION",
                    },
                },
                "quantity": 1,
            }
        )
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)

def payment_completed_premium_particular(request):
    particular = Particular.objects.get(user=request.user)
    particular.is_subscribed = True
    particular.save()
    return render(request, "payment/completed.html")
