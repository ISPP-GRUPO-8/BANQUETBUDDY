from django.shortcuts import render, redirect
from banquetBuddy import settings
from catering_employees.models import Employee
from catering_particular.models import Particular

from catering_owners.models import CateringCompany
from .forms import EmailAuthenticationForm


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .forms import ErrorForm

from django.contrib import messages
from .models import CustomUser
from catering_owners.models import CateringService, Offer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from random import sample
from django.utils import timezone
from datetime import timedelta
from catering_owners.models import NotificationEvent, NotificationJobApplication
from catering_owners.models import Event

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str


def get_user_type(user):
    try:
        particular = Particular.objects.get(user_id=user.id)
        return "Particular"
    except Particular.DoesNotExist:
        pass

    try:
        catering_company = CateringCompany.objects.get(user_id=user.id)
        return "Catering Company"
    except CateringCompany.DoesNotExist:
        pass

    try:
        employee = Employee.objects.get(user_id=user.id)
        return "Employee"
    except Employee.DoesNotExist:
        pass

    return "Unknown"


def home(request):
    context = {}
    offers = Offer.objects.all()
    random_offers = sample(list(offers), 4)

    caterings = CateringService.objects.all()
    random_caterings = sample(list(caterings), 4)

    context["offers"] = random_offers
    context["caterings"] = random_caterings
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    return render(request, "core/home.html", context)


def is_particular(request):
    try:
        particular = Particular.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_catering_company(request):
    try:
        catering_company = CateringCompany.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_catering_company_not_subscribed(request):
    try:
        catering_company = CateringCompany.objects.get(
            user=request.user, price_plan="NO_SUBSCRIBED"
        )
        res = True
    except:
        res = False
    return res


def is_catering_company_basic(request):
    try:
        catering_company = CateringCompany.objects.get(
            user=request.user, price_plan="BASIC"
        )
        res = True
    except:
        res = False
    return res


def is_catering_company_premium(request):
    try:
        catering_company = CateringCompany.objects.get(
            user=request.user, price_plan="PREMIUM"
        )
        res = True
    except:
        res = False
    return res


def is_catering_company_premium_pro(request):
    try:
        catering_company = CateringCompany.objects.get(
            user=request.user, price_plan="PREMIUM_PRO"
        )
        res = True
    except:
        res = False
    return res


def home(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    return render(request, "core/home.html", context)


def is_particular(request):
    try:
        particular = Particular.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_catering_company(request):
    try:
        catering_company = CateringCompany.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_particular(request):
    try:
        particular = Particular.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def is_catering_company(request):
    try:
        catering_company = CateringCompany.objects.get(user=request.user)
        res = True
    except:
        res = False
    return res


def about_us(request):
    return render(request, "core/aboutus.html")


def subscription_plans(request):
    if is_catering_company(request):
        catering_company = CateringCompany.objects.get(user=request.user)
        return render(
            request,
            "core/subscriptionsplans.html",
            {"price_plan": catering_company.price_plan},
        )
    return render(request, "core/subscriptionsplans.html")


def faq(request):
    return render(request, "core/faq.html")


def contact(request):
    return render(request, "core/contact.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        form = EmailAuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Comprueba si el usuario es particular o empresa
            try:
                particular_username = request.user.ParticularUsername
                is_particular = True
            except:
                is_particular = False
            try:
                company_username = request.user.CateringCompanyusername
                is_company = True
            except:
                is_company = False

            if is_particular:
                send_notifications_next_events_particular(request)
            elif is_company:
                send_notifications_next_events_catering_company(request)
            return redirect("/")
    else:
        # Si la solicitud no es POST, crea un nuevo formulario vacío
        form = EmailAuthenticationForm()
    # Renderiza la plantilla de inicio de sesión con el formulario
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def elegir_registro(request):
    return render(request, "core/elegir_registro.html")


@login_required
def profile_view(request):
    context = {}
    context["user"] = request.user

    # Verificar si el usuario tiene una empresa de catering asociada
    catering_company = CateringCompany.objects.filter(user=request.user).first()
    if catering_company:
        context["catering_company"] = catering_company
        print(
            "Catering Company:", catering_company
        )  # Imprimir información de depuración

    return render(request, "core/profile.html", context)


import re

import re

@login_required
def profile_edit_view(request):
    context = {"user": request.user}

    is_employee = hasattr(request.user, "EmployeeUsername")
    if is_employee:
        employee_instance = Employee.objects.get(user=request.user)
    else:
        employee_instance = None

    if request.method == "POST":
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        experience = request.POST.get("experience", "")
        profession = request.POST.get("profession", "")

        # Pasar valores al contexto
        context["email"] = email
        context["username"] = username
        context["first_name"] = first_name
        context["last_name"] = last_name
        context["experience"] = experience
        context["profession"] = profession

        # Validaciones
        if not (email and username and first_name and last_name):
            messages.error(request, "Complete all fields")
            return render(request, "core/profile_edit.html", context)

        if (
            CustomUser.objects.filter(email=email)
            .exclude(username=request.user.username)
            .exists()
        ):
            messages.error(request, "Email is already in use")
            return render(request, "core/profile_edit.html", context)

        if (
            CustomUser.objects.filter(username=username)
            .exclude(username=request.user.username)
            .exists()
        ):
            messages.error(request, "Username is already in use")
            return render(request, "core/profile_edit.html", context)

        if not re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$", first_name) or not re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$", last_name):
            messages.error(request, "First name and last name can only contain letters and spaces")
            return render(request, "core/profile_edit.html", context)

        if len(first_name) < 3  or len(last_name) < 3:
            messages.error(request, "First name and last name must be at least 3 characters long")
            return render(request, "core/profile_edit.html", context)
        
        if len(first_name) > 149  or len(last_name) > 149:
            messages.error(request, "First name and last name must have less than 150 characters")
            return render(request, "core/profile_edit.html", context)

        if is_employee:
            curriculum_file = request.FILES.get("curriculum")
            if curriculum_file:
                if not curriculum_file.name.endswith(".pdf"):
                    messages.error(request, "Please upload only PDF files")
                    return render(request, "core/profile_edit.html", context)
                if employee_instance.curriculum:
                    employee_instance.curriculum.delete()
                employee_instance.curriculum = curriculum_file
                employee_instance.save()

            if not experience or not profession:
                messages.error(request, "Please provide both experience and profession")
                return render(request, "core/profile_edit.html", context)

            employee_instance.experience = experience
            employee_instance.profession = profession
            employee_instance.save()

        user = request.user
        user.email = email
        user.first_name = first_name
        user.username = username
        user.last_name = last_name
        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect("profile")

    return render(request, "core/profile_edit.html", context)




@login_required
def error_report(request):
    if request.method == "POST":
        form = ErrorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            message = form.cleaned_data["message"]
            reporter_email = form.cleaned_data["reporter_email"]
            error_type = form.cleaned_data["error_type"]

            email = "banquetbuddyoficial@gmail.com"

            client_type = get_user_type(request.user)

            error_type_display = dict(form.fields["error_type"].choices)[error_type]

            contenido_correo = f"Name: {name} {surname} | Client Type: {client_type} | Contact Mail: {reporter_email} | Error type: {error_type_display} | Mensaje: {message}"

            subject = "Error Report"
            message = contenido_correo
            from_email = "banquetbuddyoficial@gmail.com"
            to_email = [email]

            send_mail(subject, message, from_email, to_email, html_message=message)

            return redirect("/error-report-send")
    else:
        form = ErrorForm()

    return render(request, "core/error_report.html", {"form": form})

def error_report_send(request):
    return render(request, "core/error_report_send.html")

def listar_caterings_home(request):
    context = {}
    busqueda = ""
    caterings = CateringService.objects.all()
    busqueda = request.POST.get("buscar", "")
    if busqueda:
        caterings = CateringService.objects.filter(name__icontains=busqueda)

    context["buscar"] = busqueda
    context["caterings"] = caterings
    return render(request, "listar_caterings.html", context)


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if the email belongs to an existing user
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            if user:
                # Generate password reset token and send email
                user.generate_reset_password_token()
                send_reset_password_email(user.email, user.reset_password_token)
                messages.success(
                    request,
                    "An email has been sent with instructions to reset your password.",
                )
                return redirect("reset_password")
            else:
                messages.error(request, "There is no user with this email address.")
    else:
        form = PasswordResetForm()
    return render(request, "core/reset_password.html", {"form": form})


def send_reset_password_email(email, token):
    subject = "Reset Password"
    message = f"Go to the following link to reset your password:\n\n{settings.BASE_URL}/reset_password/{token}"
    sender = settings.DEFAULT_FROM_EMAIL
    recipient = [email]
    send_mail(subject, message, sender, recipient)


def reset_password_confirm(request, token):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password_confirm", token=token)
        else:
            try:
                # Find user with provided token
                user = CustomUser.objects.get(reset_password_token=token)
                user.set_password(password1)
                user.reset_password_token = None
                user.save()
                if request.user.is_authenticated:
                    update_session_auth_hash(request, user)
                messages.success(request, "Your password has been successfully reset.")
                return redirect("login")
            except CustomUser.DoesNotExist:
                messages.error(request, "The password reset token is invalid.")
                return redirect("reset_password")
    else:
        try:
            # Find user with provided token
            user = CustomUser.objects.get(reset_password_token=token)
            return render(request, "core/reset_password_confirm.html", {"token": token})
        except CustomUser.DoesNotExist:
            messages.error(request, "The password reset token is invalid.")
            return redirect("reset_password")


def reset_password_complete(request):
    return redirect(reverse("login"))


def notification_view(request):

    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
        notifications = NotificationJobApplication.objects.filter(user=current_user)
    except Employee.DoesNotExist:
        notifications = NotificationEvent.objects.filter(user=current_user)
    context = {"notifications": notifications}

    return render(request, "core/notifications.html", context)


# Notification check functions


def send_notifications_next_events_particular(request):
    current_user = request.user
    week_after = timezone.now() + timedelta(days=7)
    next_events = Event.objects.filter(
        date__lte=week_after, particular__user=current_user
    )

    for event in next_events:

        if not event.notified_to_particular:
            message = (
                f"Your event is prepared for {event.date}. ¡Don't forget to get ready!"
            )
            NotificationEvent.objects.create(
                user=current_user, message=message, event=event
            )
            event.notified_to_particular = True
            event.save()


def send_notifications_next_events_catering_company(request):
    current_user = request.user
    week_after = timezone.now() + timedelta(days=7)
    catering_company = get_object_or_404(CateringCompany, user=current_user)
    next_events = Event.objects.filter(
        date__lte=week_after, cateringservice__cateringcompany=catering_company
    )

    for event in next_events:

        if not event.notified_to_catering_company:
            message = f"There is an upcoming event on {event.date}. ¡Make sure everything is prepared!"
            NotificationEvent.objects.create(
                user=current_user, message=message, event=event
            )
            event.notified_to_catering_company = True
            event.save()


def actual_privacy_policy(request):
    return render(request, "core/actual_privacy_policy.html")


def actual_terms_and_conditions(request):
    return render(request, "core/actual_terms_and_conditions.html")


def previous_policies(request):
    return render(request, "core/previous_policies.html")


def previous_terms(request):
    return render(request, "core/previous_terms.html")


def policy_archive(request):
    return render(request, "core/previous_policies.html")


def terms_archive(request):
    return render(request, "core/previous_terms.html")


def policy_version1_0(request):
    return render(request, "core/politicas y terminos anteriores/policyv1_0.html")


def terms_version1_0(request):
    return render(request, "core/politicas y terminos anteriores/termsv1.0.html")


# Borrado de notificaciones
def mark_notifications_as_read(request):
    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
        notifications = NotificationJobApplication.objects.filter(user=current_user)
    except Employee.DoesNotExist:
        notifications = NotificationEvent.objects.filter(user=current_user)

    for notification in notifications:
        notification.delete()

    return redirect("notifications")


# Método para activar la cuenta del usuario
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("login")
        else:
            return render(request, "activation_invalid.html")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, "activation_invalid.html")
