from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from core.views import is_catering_company
from .forms import (
    CateringServiceFilterForm,
    CateringServiceForm,
    OfferForm,
    CateringCompanyForm,
    MenuForm,
    EmployeeFilterForm,
)
from django.http import HttpResponseForbidden
from .models import Offer, CateringService, Event
from django.contrib.auth.decorators import login_required
from core.forms import CustomUserCreationForm
from .models import CateringCompany, Menu, Plate
from core.models import *
from django.db.models import Min
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.utils.dateformat import DateFormat
import calendar


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
    return render(request, "list_menus.html", {"menus": menus})


@login_required
def employee_applications(request, offer_id):

    offer = get_object_or_404(Offer, id=offer_id)

    if request.user != offer.cateringservice.cateringcompany.user:
        return render(
            request,
            "error.html",
            {"message": "No tienes permisos para acceder a esta oferta"},
        )

    applicants = offer.job_applications.select_related("employee").all()

    filter_form = EmployeeFilterForm(request.GET or None)
    if filter_form.is_valid():
        applicants = filter_form.filter_queryset(applicants)

    context = {"applicants": applicants, "offer": offer, "filter_form": filter_form}
    return render(request, "applicants_list.html", context)


@login_required
def view_reservations(request, catering_service_id):

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
        return HttpResponseForbidden(
            "You don't have permission to view this reservations."
        )


@login_required
def view_reservation(request, event_id, catering_service_id):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        event = get_object_or_404(Event, pk=event_id)
        return render(request, "view_reservation.html", {"event": event})
    else:
        return HttpResponseForbidden(
            "You don't have permission to view this reservation."
        )


@login_required
def catering_calendar_preview(request):
    catering_company = CateringCompany.objects.get(user=request.user)
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

    context = {"form": form, "year": datetime.now().year, "month": datetime.now().month}

    return render(request, "catering_calendar_home.html", context)


@login_required
def my_bookings_preview(request):
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
        return HttpResponseForbidden("You don't have permission to view this calendar.")


@login_required
def reservations_for_day(request, catering_service_id, year, month, day):
    catering_service = CateringService.objects.get(pk=catering_service_id)
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
        return HttpResponseForbidden(
            "You don't have permission to view this day reservations."
        )


def next_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        next_month = int(month) + 1
        next_year = int(year)
        if next_month > 12:
            next_month = 1
            next_year += 1
    else:
        return HttpResponseForbidden(
            "You don't have permission to manipulate this calendar."
        )

    return redirect(
        "catering_calendar",
        catering_service_id=catering_service_id,
        year=next_year,
        month=next_month,
    )


def prev_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        prev_month = int(month) - 1
        prev_year = int(year)
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
    else:
        return HttpResponseForbidden(
            "You don't have permission to manipulate this calendar."
        )

    return redirect(
        "catering_calendar",
        catering_service_id=catering_service_id,
        year=prev_year,
        month=prev_month,
    )


@login_required
def add_menu(request):
    catering_company = CateringCompany.objects.get(user=request.user)
    if request.method == "POST":
        form = MenuForm(request.user, request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.cateringcompany = catering_company
            menu.save()
            messages.success(request, "Menu created successfully..")
            return redirect("list_menus")
    else:
        form = MenuForm(request.user)

    return render(request, "add_menu.html", {"form": form})


@login_required
def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=request.user)
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
    menu = get_object_or_404(Menu, id=menu_id, cateringcompany__user=request.user)
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


###########################
######### Ofertas #########
###########################


@login_required
def offer_list(request):

    current_user = request.user

    try:
        catering_company = CateringCompany.objects.get(user=current_user)
    except CateringCompany.DoesNotExist:
        return render(request, "error_catering.html")

    offers = Offer.objects.filter(cateringservice__cateringcompany=catering_company)
    return render(request, "offers/offer_list.html", {"offers": offers})


@login_required
def create_offer(request):
    catering_company = request.user.CateringCompanyusername
    catering_services = CateringService.objects.filter(cateringcompany=catering_company)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.cateringservice = CateringService.objects.get(
                pk=request.POST["catering_service"]
            )  # Obtener el CateringService seleccionado en el formulario
            offer.save()
            return redirect("offer_list")
    else:
        form = OfferForm()

    return render(
        request,
        "offers/create_offer.html",
        {"form": form, "catering_services": catering_services},
    )


@login_required
def edit_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user == offer.cateringservice.cateringcompany.user:
        if request.method == "POST":
            form = OfferForm(request.POST, instance=offer)
            if form.is_valid():
                form.save()
                return redirect("offer_list")
        else:
            form = OfferForm(instance=offer)
        return render(request, "offers/edit_offer.html", {"form": form, "offer": offer})
    else:
        return redirect("offer_list")


def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, "offers/delete_offer.html", {"offer": offer})


@login_required
def confirm_delete_offer(request, offer_id):
    if request.method == "POST":
        offer = get_object_or_404(Offer, pk=offer_id)
        offer.delete()
        return redirect("offer_list")
    else:
        return redirect("offer_list")


def apply_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            # Procesar la aplicación, por ejemplo, guardarla en la base de datos
            application = form.save(commit=False)
            application.offer = offer  # Asignar la oferta a la aplicación
            application.save()
            # Aquí podrías agregar cualquier lógica adicional, como enviar un correo electrónico de confirmación
            return redirect(
                "offer_list"
            )  # Redirigir de vuelta a la lista de ofertas después de aplicar
    else:
        form = OfferForm()

    return render(request, "offers/offer_list.html", {"form": form, "offer": offer})


###########################
######## Servicios ########
###########################


@login_required
def get_catering_services(request):
    context = {}
    catering_company = CateringCompany.objects.get(user=request.user)
    services = CateringService.objects.filter(cateringcompany=catering_company)
    context["services"] = services
    context["is_catering_company"] = is_catering_company(request)
    return render(request, "list_my_services.html", context)


@login_required
def create_catering_service(request):
    context={}
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
    context={}
    context["is_catering_company"] = is_catering_company(request)
    catering_service = get_object_or_404(CateringService, id=service_id)

    if catering_service.cateringcompany.user != request.user:
        return HttpResponseForbidden("No tienes permiso para actualizar este servicio.")

    if request.method == "POST":
        form = CateringServiceForm(request.POST, instance=catering_service)
        if form.is_valid():
            form.save()
            return redirect("services")
    else:
        form = CateringServiceForm(instance=catering_service)
    context["form"] = form
    context["service"] = catering_service
    return render(request, "edit_catering_service.html", context)

@login_required
def delete_service(request, service_id):
    context={}
    context["is_catering_company"] = is_catering_company(request)
    service = get_object_or_404(CateringService, pk=service_id)
    context["service"] = service
    return render(request, "delete_service.html", context)

@login_required
def confirm_delete_service(request, service_id):
    if request.method == "POST":
        service = get_object_or_404(CateringService, pk=service_id)
        service.delete()
        return redirect("services")  
    else:
        return redirect("services")  