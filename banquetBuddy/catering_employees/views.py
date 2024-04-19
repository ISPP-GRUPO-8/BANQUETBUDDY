from django.shortcuts import render, redirect
from django.contrib import messages

from catering_owners.models import (
    CateringCompany,
    Offer,
    JobApplication,
    RecommendationLetter,
)
from .models import Employee
from .forms import EmployeeFilterForm, EmployeeForm
from core.views import *

from core.forms import CustomUserCreationForm
from catering_owners.models import JobApplication, Employee, EmployeeWorkService
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, Value, CharField
from django.http import HttpResponseForbidden
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from core.permission_checks import is_user_employee
from django.core.paginator import Paginator


# Create your views here.


NOT_EMPLOYEE_ERROR = "You are not registered as an employee"
FORBIDDEN_ACCESS_ERROR = "You are not allowed to access to the following page"


def register_employee(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        curriculum_file = request.FILES.get("curriculum")
        if curriculum_file:
            if not curriculum_file.name.endswith(".pdf"):
                messages.error(request, "Por favor, carga solo archivos PDF")
                return render(
                    request,
                    "core/registro_empleado.html",
                    {"user_form": user_form, "employee_form": employee_form},
                )

        if user_form.is_valid() and employee_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = (
                False  # Desactiva la cuenta hasta que se confirme el correo electrónico
            )
            user.save()

            employee_profile = employee_form.save(commit=False)
            employee_profile.user = user
            employee_profile.curriculum = curriculum_file
            employee_profile.save()

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
                "Registration successful! Please confirm your email address to complete the registration",
            )

            return redirect("home")

    else:
        user_form = CustomUserCreationForm()
        employee_form = EmployeeForm()

    return render(
        request,
        "core/registro_empleado.html",
        {"user_form": user_form, "employee_form": employee_form},
    )


@login_required
def employee_applications(request, offer_id):

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
def employee_offer_list(request):
    context = {}

    current_user = request.user
    offers = Offer.objects.all()

    if not is_user_employee(current_user):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)

    employee = Employee.objects.get(user=current_user)
    search = ""
    offers = Offer.objects.all()
    if request.method == "POST":
        search = request.POST.get("search", "")
        if search:
            offers = Offer.objects.filter(Q(title__icontains=search))

    applications = {
        offer.id: offer.job_applications.filter(employee=employee).exists()
        for offer in offers
    }
    hirings = {
        offer.id: EmployeeWorkService.objects.filter(
            employee=employee, cateringservice=offer.cateringservice
        ).exists()
        for offer in offers
    }
    context = {
        "offers": offers,
        "applications": applications,
        "search": search,
        "hirings": hirings,
    }

    return render(request, "employee_offer_list.html", context)


@login_required
def application_to_offer(request, offer_id):

    current_user = request.user
    if not is_user_employee(current_user):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)
    employee = Employee.objects.get(user=current_user)

    offer = get_object_or_404(Offer, id=offer_id)

    if JobApplication.objects.filter(
        employee=employee, offer=offer
    ) or EmployeeWorkService.objects.filter(
        employee=employee, cateringservice=offer.cateringservice
    ):
        return render(request, "error_employee_already_applied.html")
    elif not employee.curriculum:
        return render(request, "error_employee_curriculum.html")
    else:
        JobApplication.objects.create(employee=employee, offer=offer, state="PENDING")
        return render(request, "application_success.html")


@login_required
def employee_applications_list(request):

    current_user = request.user
    if not is_user_employee(current_user):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)

    employee = Employee.objects.get(user=current_user)
    applications = JobApplication.objects.filter(employee=employee)
    context = {"applications": applications}

    return render(request, "application_employee_list.html", context)


@login_required
def my_recommendation_letters(request, employee_id):
    current_user = request.user
    if not is_user_employee(current_user):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)
    employee = Employee.objects.get(user=current_user)
    if employee.user.id != employee_id:
        return HttpResponseForbidden(FORBIDDEN_ACCESS_ERROR)

    recommendations = RecommendationLetter.objects.filter(employee_id=employee_id)

    recommendation_dict = {}
    for recommendation in recommendations:
        catering_company = CateringCompany.objects.get(
            user_id=recommendation.catering_id
        )
        recommendation_dict[recommendation] = catering_company

    context = {"recommendation_dict": recommendation_dict}

    return render(request, "my_recommendation_letters.html", context)


@login_required
def listar_caterings_companies(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    if not is_employee(request):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)
    caterings = CateringCompany.objects.all()

    context["caterings"] = caterings
    return render(request, "contact_chat_employee.html", context)


@login_required
def list_work_services(request):
    current_user = request.user
    if not is_user_employee(current_user):
        return HttpResponseForbidden(NOT_EMPLOYEE_ERROR)
    employee = Employee.objects.get(user_id=current_user.id)
    status_filter = request.GET.get(
        "status", "Activo"
    )  # 'Activo' es el valor predeterminado
    employee_services = (
        EmployeeWorkService.objects.filter(employee=employee)
        .annotate(
            current_status=Case(
                When(end_date__isnull=True, then=Value("Activo")),
                When(end_date__lte=timezone.now().date(), then=Value("Terminado")),
                default=Value("Activo"),
                output_field=CharField(),
            )
        )
        .filter(current_status=status_filter)
        .order_by("-start_date")
    )

    paginator = Paginator(employee_services, 10)  # Muestra 10 servicios por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "list_work_services.html",
        {"page_obj": page_obj, "current_status": status_filter},
    )
