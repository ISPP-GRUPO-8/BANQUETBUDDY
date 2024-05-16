from datetime import datetime, date
import calendar
from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, CharField
from core.views import *
from .forms import (
    OfferForm,
    CateringCompanyForm,
    MenuForm,
    EmployeeWorkServiceForm,
    TaskForm,
    TerminationForm,
)
from .forms import (
    CateringServiceFilterForm,
    OfferForm,
    CateringCompanyForm,
    MenuForm,
    EmployeeFilterForm,
)
from django.http import HttpResponseForbidden
from .models import Offer, CateringService, Event, Employee, EmployeeWorkService
from urllib.parse import urlencode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Min
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.dateformat import DateFormat
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import traceback
import logging

logger = logging.getLogger(__name__)
from django.db import transaction
from django.db.models import Case, When, Value, CharField
import json

from core.views import is_catering_company
from .forms import (
    CateringCompanyForm,
    CateringServiceFilterForm,
    CateringServiceForm,
    EmployeeFilterForm,
    MenuForm,
    OfferForm,
    PlateForm,
)
from .models import (
    Offer,
    CateringService,
    Event,
    Employee,
    EmployeeWorkService,
    CateringCompany,
    Menu,
    Plate,
)
from core.views import is_catering_company
from core.permission_checks import is_user_catering_company
from core.views import *

from catering_owners.models import *
from .forms import TerminationForm
from core.forms import CustomUserCreationForm

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

NOT_CATERING_COMPANY_ERROR = "You are not registered as a catering company"
FORBIDDEN_ACCESS_ERROR = "You are not allowed to access to the following page"


@login_required
def catering_books(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    catering_company = get_object_or_404(CateringCompany, user=current_user)
    catering_services = CateringService.objects.filter(
        cateringcompany_id=catering_company.user_id
    )
    events = Event.objects.filter(cateringservice__in=catering_services)
    context = {"events": events}
    return render(request, "particular_books.html", context)


@login_required
def book_catering_cancel(request, event_id):
    user = request.user
    catering_company = get_object_or_404(CateringCompany, user=user)
    catering_service = CateringService.objects.filter(cateringcompany=catering_company)
    event = get_object_or_404(Event, id=event_id)
    if event.cateringservice.cateringcompany.user != user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    for service in catering_service:
        if user == service.cateringcompany.user:
            event.booking_state = BookingState.CANCELLED
            event.save()

    return redirect("catering_books")


@login_required
def book_catering_edit(request, event_id):
    current_user = request.user
    event = get_object_or_404(Event, id=event_id)
    if event.cateringservice.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    catering_company = get_object_or_404(CateringCompany, user=request.user)
    menus = Menu.objects.filter(cateringcompany=catering_company)
    context = {"event": event, "menus": menus}

    if request.method == "POST":
        date = request.POST.get("date")
        number_guests = request.POST.get("number_guests")
        menu = request.POST.get("selected_menu")

        if number_guests == "0":
            context["error"] = "The number of guests can not be 0."
            return render(request, "catering_book_edit.html", context)

        date2 = datetime.strptime(date, "%Y-%m-%d").date()

        if datetime.now().date() > date2:
            context["error"] = "The selected date cannot be in the past."
            return render(request, "catering_book_edit.html", context)

        event.date = date
        event.number_guests = number_guests
        event.menu = Menu.objects.get(id=int(menu))
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f"Reservation for {number_guests} guests"
        event.save()

        return redirect("catering_books")

    return render(request, "catering_book_edit.html", context)


def register_company(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        company_form = CateringCompanyForm(request.POST, request.FILES)

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = (
                False  # Desactiva la cuenta hasta que se confirme el correo electrónico
            )
            user.save()

            company_profile = company_form.save(commit=False)
            company_profile.user = user
            company_profile.price_plan = PricePlan.NO_SUBSCRIBED
            company_profile.save()

            # Genera un token único para el usuario
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Obtiene el dominio actual
            domain = get_current_site(request).domain
            # Crea el enlace de confirmación
            link = f"http://{domain}/activate/{uid}/{token}"
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
                "Registration successful! Please check your email to activate you account",
            )

            return redirect("home")

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
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=current_user)
    menus_query = Menu.objects.filter(cateringcompany=catering_company)

    # Paginación
    paginator = Paginator(menus_query, 9)
    page_number = request.GET.get("page")
    menus = paginator.get_page(page_number)

    return render(request, "list_menus.html", {"menus": menus})


@login_required
def employee_applications(request, offer_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    offer = get_object_or_404(Offer, id=offer_id)

    if request.user != offer.cateringservice.cateringcompany.user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    applicants = offer.job_applications.select_related("employee").all()

    filter_form = EmployeeFilterForm(request.GET or None)
    if filter_form.is_valid():
        applicants = filter_form.filter_queryset(applicants)

    context = {"applicants": applicants, "offer": offer, "filter_form": filter_form}
    return render(request, "applicants_list.html", context)


@login_required
def view_reservations(request, catering_service_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        catering_service = get_object_or_404(CateringService, pk=catering_service_id)
        reservations = catering_service.events.all()
        return render(
            request,
            "reservations.html",
            {"reservations": reservations, "catering_service": catering_service},
        )
    else:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)


@login_required
def view_reservation(request, event_id, catering_service_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        event = get_object_or_404(Event, pk=event_id)
        return render(request, "view_reservation.html", {"event": event})
    else:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)


@login_required
def catering_calendar_preview(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=request.user)
    if is_catering_company_premium(request) or is_catering_company_premium_pro(request):
        if request.method == "POST":
            form = CateringServiceFilterForm(catering_company, request.POST)
            if form.is_valid():
                selected_catering_service = form.cleaned_data.get("catering_service")
                if selected_catering_service:
                    return redirect(
                        "catering_calendar",
                        year=datetime.now().year,
                        month=datetime.now().month,
                        catering_service_id=selected_catering_service.id,
                    )
        else:
            form = CateringServiceFilterForm(catering_company)
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")

    context = {"form": form, "year": datetime.now().year, "month": datetime.now().month}

    return render(request, "catering_calendar_home.html", context)


@login_required
def my_bookings_preview(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=request.user)
    if request.method == "POST":
        form = CateringServiceFilterForm(catering_company, request.POST)
        if form.is_valid():
            selected_catering_service = form.cleaned_data.get("catering_service")
            if selected_catering_service:
                return redirect(
                    "view_reservations",
                    catering_service_id=selected_catering_service.id,
                )
    else:
        form = CateringServiceFilterForm(catering_company)

    context = {
        "form": form,
    }

    return render(request, "catering_calendar_home.html", context)


@login_required
def catering_calendar_view(request, catering_service_id, month, year):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if is_catering_company_premium(request) or is_catering_company_premium_pro(request):
        if request.user == catering_service.cateringcompany.user:
            month = min(
                max(int(month), 1), 12
            )  # Asegurarse de que el mes esté en el rango válido (1-12)
            month_name = DateFormat(datetime(year, month, 1)).format("F")

            # Obtener el calendario del mes y los días con eventos
            cal = calendar.monthcalendar(year, month)
            events = Event.objects.filter(
                cateringservice=catering_service, date__year=year, date__month=month
            ).values_list("date__day", flat=True)

            num_events = events.count()
            next_event_date = Event.objects.filter(
                cateringservice=catering_service,
                date__gte=date.today(),  # Solo eventos futuros
            ).aggregate(next_event=Min("date"))["next_event"]
            if next_event_date is None:
                next_event_date = "No upcoming events"
            else:
                next_event_date = next_event_date.strftime("%Y-%m-%d")
            # Generar una lista de días con eventos para resaltar en el calendario

            event_days = set(events)
            return render(
                request,
                "calendar.html",
                {
                    "catering_name": catering_service.name,
                    "catering_service_id": catering_service_id,
                    "year": year,
                    "month": month,
                    "month_name": month_name,
                    "cal": cal,
                    "event_days": event_days,
                    "next_event_date": next_event_date,
                    "num_events": num_events,
                },
            )
        else:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")


@login_required
def reservations_for_day(request, catering_service_id, year, month, day):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if is_catering_company_premium(request) or is_catering_company_premium_pro(request):
        if request.user == catering_service.cateringcompany.user:
            selected_date = datetime(year, month, day)
            reservations = Event.objects.filter(
                cateringservice=catering_service, date=selected_date
            )
            return render(
                request,
                "reservations_for_day.html",
                {
                    "catering_service": catering_service,
                    "selected_date": selected_date,
                    "reservations": reservations,
                },
            )
        else:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")


def next_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if is_catering_company_premium(request) or is_catering_company_premium_pro(request):
        if request.user == catering_service.cateringcompany.user:
            next_month = int(month) + 1
            next_year = int(year)
            if next_month > 12:
                next_month = 1
                next_year += 1
        else:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")

    return redirect(
        "catering_calendar",
        catering_service_id=catering_service_id,
        year=next_year,
        month=next_month,
    )


def prev_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if is_catering_company_premium(request) or is_catering_company_premium_pro(request):
        if request.user == catering_service.cateringcompany.user:
            prev_month = int(month) - 1
            prev_year = int(year)
            if prev_month < 1:
                prev_month = 12
                prev_year -= 1
        else:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")

    return redirect(
        "catering_calendar",
        catering_service_id=catering_service_id,
        year=prev_year,
        month=prev_month,
    )


@login_required
def add_menu(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=request.user)
    if request.method == "POST":
        form = MenuForm(request.user, request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.cateringcompany = catering_company
            menu.save()
            messages.success(request, "Menu created successfully.")
            return redirect("list_menus")
    else:
        form = MenuForm(request.user)

    return render(request, "add_menu.html", {"form": form})


@login_required
def edit_menu(request, menu_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=current_user)
    if request.method == "POST":
        form = MenuForm(request.user, request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu updated successfully.")
            return redirect("list_menus")
    else:
        form = MenuForm(request.user, instance=menu)
    return render(request, "edit_menu.html", {"form": form})


@login_required
def delete_menu(request, menu_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=current_user)
    if request.method == "POST":
        menu.delete()
        messages.success(request, "Menu removed successfully.")
        return redirect("list_menus")
    else:
        return redirect("list_menus")


@login_required
def catering_profile_edit(request):
    context = {}
    user = request.user
    if not is_user_catering_company(user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    # Obtener el perfil de la empresa de catering del usuario actual
    catering_company = CateringCompany.objects.get_or_create(user=user)[0]

    if request.method == "POST":
        form = CateringCompanyForm(
            request.POST, request.FILES, instance=catering_company
        )
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


@login_required
def catering_unsuscribe(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    catering_company.price_plan = "NO_SUBSCRIBED"
    catering_company.save()
    return redirect("profile")


@login_required
def payment_process_base(request):
    success_url = request.build_absolute_uri(reverse("completed_base"))
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
                "unit_amount": int(999),
                "currency": "eur",
                "product_data": {
                    "name": f"BASE PLAN SUBSCRIPTION",
                },
            },
            "quantity": 1,
        }
    )
    # create Stripe checkout session
    session = stripe.checkout.Session.create(**session_data)
    # redirect to Stripe payment form
    return redirect(session.url, code=303)


def payment_completed_base(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    catering_company.price_plan = PricePlan.BASE
    catering_company.save()
    return render(request, "payment/completed.html")


@login_required
def payment_process_premium(request):
    success_url = request.build_absolute_uri(reverse("completed_premium"))
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
                "unit_amount": int(1999),
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


def payment_completed_premium(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    catering_company.price_plan = PricePlan.PREMIUM
    catering_company.save()
    return render(request, "payment/completed.html")


@login_required
def payment_process_pro(request):
    success_url = request.build_absolute_uri(reverse("completed_pro"))
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
                "unit_amount": int(2999),
                "currency": "eur",
                "product_data": {
                    "name": f"PREMIUM PRO PLAN SUBSCRIPTION",
                },
            },
            "quantity": 1,
        }
    )
    # create Stripe checkout session
    session = stripe.checkout.Session.create(**session_data)
    # redirect to Stripe payment form
    return redirect(session.url, code=303)


def payment_completed_pro(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    catering_company.price_plan = PricePlan.PREMIUM_PRO
    catering_company.save()
    return render(request, "payment/completed.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")


###########################
######### Ofertas #########
###########################


@login_required
def offer_list(request):

    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=current_user)
    if is_catering_company_premium_pro(request) is True:
        offers = Offer.objects.filter(cateringservice__cateringcompany=catering_company)
        return render(request, "offers/offer_list.html", {"offers": offers})
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")


@login_required
def create_offer(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = request.user.CateringCompanyusername
    events = Event.objects.filter(cateringcompany=catering_company)
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.cateringservice = offer.event.cateringservice
            offer.save()
            messages.success(request, "Offer created successfully!")
            return redirect("offer_list")

    else:
        form = OfferForm()

    return render(request, "offers/create_offer.html", {"form": form, "events": events})


@login_required
def edit_offer(request, offer_id):
    current_user = request.user
    offer = get_object_or_404(Offer, pk=offer_id)

    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    if current_user != offer.cateringservice.cateringcompany.user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    catering_company = request.user.CateringCompanyusername
    events = Event.objects.filter(cateringcompany=catering_company)

    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            try:
                form.save()  # Intenta guardar el formulario
                messages.success(request, "Offer updated successfully.")
                return redirect("offer_list")
            except ValidationError as e:
                # Añade los errores de validación del modelo a los errores del formulario
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
        # Si la validación falla, pasa el formulario con errores al template
    else:
        messages.error(request, "Please correct the errors below.")

    return render(
        request,
        "offers/edit_offer.html",
        {"form": form, "offer": offer, "events": events},
    )


@login_required
def delete_offer(request, offer_id):
    if is_catering_company_premium_pro(request) is True:
        offer = get_object_or_404(Offer, pk=offer_id)
        if request.user != offer.cateringservice.cateringcompany.user:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
        return render(request, "offers/delete_offer.html", {"offer": offer})
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")


@login_required
def confirm_delete_offer(request, offer_id):
    if is_catering_company_premium_pro(request) is True:
        offer = get_object_or_404(Offer, pk=offer_id)
        if request.user != offer.cateringservice.cateringcompany.user:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
        if request.method == "POST":
            offer = get_object_or_404(Offer, pk=offer_id)
            offer.delete()
            return redirect("offer_list")
        else:
            return redirect("offer_list")
    else:
        messages.error(
            request,
            "Cant access this functionality with your current plan.Perhaps you want to check a better plan?",
        )
        return redirect("subscription_plans")


###########################
######## Servicios ########
###########################


@login_required
def get_catering_services(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    context = {}
    catering_company = CateringCompany.objects.get(user=current_user)
    services = CateringService.objects.filter(cateringcompany=catering_company)
    context["services"] = services
    context["is_catering_company"] = is_catering_company(request)
    return render(request, "list_my_services.html", context)


@login_required
def create_catering_service(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    context = {}
    context["is_catering_company"] = is_catering_company(request)
    if request.method == "POST":
        form = CateringServiceForm(request.POST)
        if form.is_valid():
            catering_service = form.save(commit=False)
            catering_service.cateringcompany = CateringCompany.objects.get(
                user=request.user
            )
            catering_service.save()
            return redirect("services")
    else:
        form = CateringServiceForm()
        context["form"] = form
    return render(request, "create_catering_service.html", context)


@login_required
def update_catering_service(request, service_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    context = {}
    context["is_catering_company"] = is_catering_company(request)
    catering_service = get_object_or_404(CateringService, id=service_id)

    if catering_service.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    if request.method == "POST":
        form = CateringServiceForm(request.POST, instance=catering_service)
        if form.is_valid():
            form.save()
            messages.success(request, "Catering Service updated successfully.")
            return redirect("services")
    else:
        form = CateringServiceForm(instance=catering_service)
    context["form"] = form
    context["service"] = catering_service
    return render(request, "edit_catering_service.html", context)


@login_required
def delete_service(request, service_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    context = {}
    context["is_catering_company"] = is_catering_company(request)
    service = get_object_or_404(CateringService, pk=service_id)
    if service.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    context["service"] = service
    return render(request, "delete_service.html", context)


@login_required
def confirm_delete_service(request, service_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    if request.method == "POST":
        service = get_object_or_404(CateringService, pk=service_id)
        if service.cateringcompany.user != current_user:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
        service.delete()
        return redirect("services")
    else:
        return redirect("services")


@login_required
def list_plates(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = get_object_or_404(CateringCompany, user=current_user)
    plates_query = Plate.objects.filter(cateringcompany=catering_company)

    # Filtrar los platos si se proporciona menu_id
    menu_id = request.GET.get("menu_id")
    if menu_id:
        if menu_id == "none":
            plates_query = plates_query.filter(menu__isnull=True)
        else:
            try:
                menu_id_int = int(menu_id)
                plates_query = plates_query.filter(menu__id=menu_id_int)
            except ValueError:
                pass

    # Guardar los parámetros del filtro en la sesión
    request.session["plate_filter"] = {"menu_id": menu_id}

    # Manejar la ordenación
    sort_by = request.GET.get("sort", "name")
    order = request.GET.get("order", "asc")
    if sort_by not in ["name", "menu", "price"]:
        sort_by = "name"
    if order == "desc":
        plates_query = plates_query.order_by("-" + sort_by)
    else:
        plates_query = plates_query.order_by(sort_by)

    # Paginación
    paginator = Paginator(plates_query, 9)
    page_number = request.GET.get("page")
    plates = paginator.get_page(page_number)

    # Obtener todos los menús para el filtro
    menus = (
        Menu.objects.filter(cateringcompany=catering_company)
        .values("id", "name")
        .distinct()
    )

    return render(
        request,
        "list_plates.html",
        {"plates": plates, "menus": menus, "selected_menu_id": menu_id},
    )


@login_required
def delete_plate(request, plate_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    plate = get_object_or_404(Plate, id=plate_id, cateringcompany__user=request.user)
    if plate.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    if request.method == "POST":
        plate.delete()
        messages.success(request, "Plate removed successfully.")

        # Recuperar los parámetros de filtro de la sesión y redireccionar
        filter_params = request.session.get("plate_filter", {})
        return redirect(f"{reverse('list_plates')}?{urlencode(filter_params)}")

    else:
        return redirect("list_plates")


@login_required
def add_plate(request):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    catering_company = CateringCompany.objects.get(user=request.user)
    if request.method == "POST":
        form = PlateForm(request.user, request.POST)
        if form.is_valid():
            plate = form.save(commit=False)
            plate.cateringcompany = catering_company
            plate.save()
            messages.success(request, "Plate created successfully.")
            return redirect("list_plates")
    else:
        form = PlateForm(request.user)

    return render(request, "add_plate.html", {"form": form})


@login_required
def edit_plate(request, plate_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)

    plate = get_object_or_404(Plate, id=plate_id, cateringcompany__user=request.user)
    if plate.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    if request.method == "POST":
        form = PlateForm(request.user, request.POST, instance=plate)
        if form.is_valid():
            form.save()
            messages.success(request, "Plate updated successfully.")
            return redirect("list_plates")
    else:
        form = PlateForm(request.user, instance=plate)
    return render(request, "edit_plate.html", {"form": form})


@login_required
def delete_plate(request, plate_id):
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    plate = get_object_or_404(Plate, id=plate_id, cateringcompany__user=current_user)
    if plate.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    if request.method == "POST":
        plate.delete()
        messages.success(request, "Plate removed successfully.")
        # Recuperar y utilizar los parámetros de filtro de la sesión
        filter_params = request.session.get("plate_filter", {})
        return redirect(f"{reverse('list_plates')}?{urlencode(filter_params)}")
    else:
        return redirect("list_plates")


@login_required
def list_employee(request, service_id):
    catering_service = get_object_or_404(CateringService, id=service_id)
    current_user = request.user
    if not is_user_catering_company(current_user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    if catering_service.cateringcompany.user != current_user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    owner = CateringCompany.objects.get(user_id=request.user.id)

    status_filter = request.GET.get("status", "Activo")
    all_employees = EmployeeWorkService.objects.filter(cateringservice=catering_service)
    filtered_employees = [
        emp for emp in all_employees if emp.current_status() == status_filter
    ]

    paginator = Paginator(filtered_employees, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    recommendations = RecommendationLetter.objects.filter(catering_id=owner.user.id)
    recommendations_dict = {
        recommendation.employee_id: recommendation for recommendation in recommendations
    }
    all_employees = EmployeeWorkService.objects.filter(cateringservice=catering_service)

    return render(
        request,
        "list_employee.html",
        {
            "page_obj": page_obj,
            "service": catering_service,
            "recommendations_dict": recommendations_dict,
            "current_status": status_filter,
        },
    )


@login_required
def edit_employee_termination(request, employee_work_service_id):
    employee_service = get_object_or_404(
        EmployeeWorkService, id=employee_work_service_id
    )
    form = TerminationForm(request.POST or None, instance=employee_service)

    if request.method == "POST":
        if form.is_valid():
            # Aquí podrías agregar una comprobación adicional, aunque no es necesaria
            termination_reason = form.cleaned_data.get("termination_reason")
            if not termination_reason:
                form.add_error("termination_reason", "This field is required.")
            else:
                form.save()
                messages.success(
                    request, "Employee termination details updated successfully."
                )
                return redirect(
                    "list_employee", service_id=employee_service.cateringservice.id
                )

    return render(
        request,
        "edit_employee.html",
        {"employee_service": employee_service, "form": form},
    )


@login_required
def create_recommendation_letter(request, employee_id, service_id):
    user = request.user
    if not is_user_catering_company(user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    catering_service = get_object_or_404(CateringService, id=service_id)
    if catering_service.cateringcompany.user != user:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
    employee = get_object_or_404(Employee, user_id=employee_id)

    try:
        owner = CateringCompany.objects.get(user_id=user.id)
        if owner:
            context = {
                "employee": employee,
                "owner": owner,
                "service": catering_service,
            }

            if request.method == "POST":
                description = request.POST.get("description")

                recommendation_letter = RecommendationLetter.objects.create(
                    employee=employee,
                    catering=owner,
                    description=description,
                    date=datetime.now().date(),
                )
                return redirect("list_employee", service_id=service_id)
    except:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    return render(request, "recommendation_letter.html", context)


def employee_record_list(request, employee_id):
    employee = get_object_or_404(Employee, user_id=employee_id)
    services_worked = EmployeeWorkService.objects.filter(employee=employee)
    return render(
        request,
        "employee_record.html",
        {"employee": employee, "services_worked": services_worked},
    )


@login_required
def hire_employee(request, employee_id):
    user = request.user
    if not is_user_catering_company(user):
        return HttpResponseForbidden(NOT_CATERING_COMPANY_ERROR)
    if request.method == "POST":
        action = request.POST.get("action")
        offer_id = request.POST.get("offer_id")
        offer = get_object_or_404(Offer, pk=offer_id)
        if offer.cateringservice.cateringcompany.user != user:
            return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)
        employee = get_object_or_404(Employee, pk=employee_id)

        if action == "hire":
            # Crear EmployeeWorkService directamente
            EmployeeWorkService.objects.create(
                employee=employee,
                cateringservice=offer.cateringservice,
                event=offer.event,
                start_date=offer.start_date,
                end_date=offer.end_date,
            )

            # Crear notificación de contratación
            message = f"You have been hired by {offer.cateringservice.cateringcompany.user.username} for the offer '{offer.title}', from {offer.start_date} to {offer.end_date}."
            NotificationJobApplication.objects.create(
                user=employee.user,
                job_application=None,
                message=message,
                title=f"Hired for {offer.title}",
            )

            # Eliminar la aplicación de trabajo si existe
            JobApplication.objects.filter(employee=employee, offer=offer).delete()

            messages.success(
                request, f"{employee.user.username} was successfully hired."
            )
            return redirect(
                "applicants", offer_id=offer_id
            )  # Redirecciona a la lista de aplicantes de la oferta

        elif action == "reject":
            # Notificar rechazo
            message = f"You have been rejected by {offer.cateringservice.cateringcompany.user.username} for the offer '{offer.title}'."
            NotificationJobApplication.objects.create(
                user=employee.user,
                job_application=None,
                message=message,
                title=f"Rejected for {offer.title}",
            )

            # Eliminar la aplicación de trabajo si existe
            JobApplication.objects.filter(employee=employee, offer=offer).delete()

            messages.error(request, f"{employee.user.username} was rejected.")
            return redirect(
                "applicants", offer_id=offer_id
            )  # Redirecciona a la lista de aplicantes de la oferta

    # Redirecciona a la lista general de ofertas si no hay acción POST
    return redirect("offer_list")


def chat_view(request, id):
    context = {}
    context["id"] = int(id)
    messages = None  # Inicializamos messages en caso de que no haya mensajes

    if is_particular(request):
        particular = Particular.objects.get(user=request.user)
        catering_company = CateringCompany.objects.get(user_id=id)

        if request.method == "POST":
            content = request.POST.get("content")
            if content:
                particular.send_message(catering_company.user, content)
                # Después de enviar el mensaje, volvemos a obtener los mensajes actualizados
                messages = particular.get_messages(catering_company.user.id)
                context["messages"] = messages
                return render(request, "chat.html", context)

        messages = particular.get_messages(catering_company.user.id)

    elif is_catering_company(request):
        try:
            particular = Particular.objects.get(user_id=id)
        except:
            pass
        try:
            particular = Employee.objects.get(user_id=id)
        except:
            pass
        catering_company = CateringCompany.objects.get(user=request.user)

        if request.method == "POST":
            content = request.POST.get("content")
            if content:
                catering_company.send_message(particular.user, content)
                # Después de enviar el mensaje, volvemos a obtener los mensajes actualizados
                messages = catering_company.get_messages(particular.user.id)
                context["messages"] = messages
                return render(request, "chat.html", context)

        messages = catering_company.get_messages(particular.user.id)

    elif is_employee(request):
        employee = Employee.objects.get(user=request.user)
        catering_company = CateringCompany.objects.get(user_id=id)

        if request.method == "POST":
            content = request.POST.get("content")
            if content:
                employee.send_message(catering_company.user, content)
                # Después de enviar el mensaje, volvemos a obtener los mensajes actualizados
                messages = employee.get_messages(catering_company.user.id)
                context["messages"] = messages
                return render(request, "chat.html", context)

        messages = employee.get_messages(catering_company.user.id)
    context["messages"] = messages
    return render(request, "chat.html", context)


@login_required
def listar_caterings_particular(request):
    context = {}
    context["is_catering_company"] = is_catering_company(request)
    catering_company = get_object_or_404(CateringCompany, user=request.user)

    messages_o = Message.objects.filter(receiver=catering_company.user)
    unique_senders = set()  # Mantener un registro de los remitentes únicos
    messages = []  # Lista para almacenar mensajes únicos

    for message in messages_o:
        sender_id = message.sender.id

        # Verificar si el remitente ya se ha encontrado antes
        if sender_id not in unique_senders:
            unique_senders.add(
                sender_id
            )  # Agregar el remitente a los remitentes únicos
            messages.append(message)  # Agregar el mensaje a la lista de mensajes únicos

    context["messages"] = messages
    return render(request, "contact_chat_owner.html", context)


@login_required
@csrf_exempt
def manage_tasks(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    task_id = request.POST.get("task_id", None)

    if event.booking_state != "CONFIRMED" or request.user != event.cateringcompany.user:
        return HttpResponseForbidden(
            "You do not have permission to manage tasks for this event."
        )

    if task_id:
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST or None, instance=task, event_id=event_id)
    else:
        form = TaskForm(request.POST or None, event_id=event_id)

    if request.method == "POST":
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.cateringservice = event.cateringservice
            task.cateringcompany = event.cateringcompany
            if not task_id:
                task.assignment_state = "PENDING"
            task.save()
            form.save_m2m()
            messages.success(
                request,
                "Task updated successfully." if task_id else "Task added successfully.",
            )
            return redirect("manage_tasks", event_id=event_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    tasks = Task.objects.filter(event=event).prefetch_related("employees")
    all_employee_work_services = EmployeeWorkService.objects.filter(
        event=event, cateringservice=event.cateringservice
    ).select_related("employee")
    active_employees = [
        ews.employee
        for ews in all_employee_work_services
        if ews.current_status() == "Activo"
    ]

    context = {
        "event": event,
        "tasks": tasks,
        "form": form,
        "active_employees": active_employees,
    }

    return render(request, "manage_tasks.html", context)


@require_POST
@login_required
@csrf_exempt
def update_task_state(request, task_id):
    try:
        if hasattr(request.user, "CateringCompanyusername"):
            catering_company = request.user.CateringCompanyusername
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "User does not have a catering company.",
                },
                status=403,
            )

        task = Task.objects.get(id=task_id, cateringcompany=catering_company)
        data = json.loads(request.body)
        new_state = data.get("newState")

        if new_state in [choice[0] for choice in AssignmentState.choices]:
            task.assignment_state = new_state
            task.save()
            return JsonResponse({"status": "success", "message": "Task state updated."})
        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid state provided."}, status=400
            )

    except Task.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Task not found."}, status=404
        )
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
    except Exception as e:
        logger.error("Error updating task state: %s", str(e), exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "Internal server error: {}".format(str(e))},
            status=500,
        )


@require_POST
@login_required
@csrf_exempt
def add_task(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = TaskForm(request.POST, event_id=event_id)

    if form.is_valid():
        with transaction.atomic():
            task = form.save(commit=False)
            task.assignment_state = "PENDING"
            task.event = event
            task.cateringservice = event.cateringservice
            task.cateringcompany = event.cateringcompany
            task.save()
            form.save_m2m()  # Guarda relaciones ManyToMany, incluyendo employees

            # Guardar empleados seleccionados en la tarea
            employees = form.cleaned_data.get("employees", [])
            task.employees.add(*employees)

        messages.success(request, "Task added successfully.")
        return redirect("manage_tasks", event_id=event_id)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

        return redirect("manage_tasks", event_id=event_id)


@require_POST
@login_required
@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(
        Task, id=task_id, cateringcompany=request.user.CateringCompanyusername
    )

    if task:
        task.delete()
        messages.success(request, "Task deleted successfully.")
    else:
        messages.error(request, "Task not found.")

    return redirect("manage_tasks", event_id=task.event.id)


def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, event_id=task.event.id)
        if form.is_valid():
            form.save()
            return redirect("manage_tasks", event_id=task.event.id)
    else:
        form = TaskForm(instance=task, event_id=task.event.id)

    return render(request, "edit_task.html", {"form": form, "task": task})


def get_task_data(request):
    task_id = request.GET.get("task_id")
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(instance=task, event_id=task.event.id)
    return render(request, "task_edit_form.html", {"form": form, "task": task})
