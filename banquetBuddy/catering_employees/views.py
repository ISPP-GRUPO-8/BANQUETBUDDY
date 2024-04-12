from django.shortcuts import render, redirect
from django.contrib import messages

from catering_owners.models import CateringCompany, Offer, JobApplication, RecommendationLetter
from .models import Employee
from .forms import EmployeeFilterForm, EmployeeForm
from core.views import *

from core.forms import CustomUserCreationForm
from catering_owners.models import JobApplication, Employee, EmployeeWorkService
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden


# Create your views here.

def register_employee(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        
        curriculum_file = request.FILES.get("curriculum")
        if curriculum_file:
            if not curriculum_file.name.endswith('.pdf'):
                messages.error(request, "Por favor, carga solo archivos PDF")
                return render(request, "core/registro_empleado.html", {"user_form": user_form, "employee_form": employee_form},)
            
        if user_form.is_valid() and employee_form.is_valid():
            
            user = user_form.save()

            employee_profile = employee_form.save(commit=False)
            employee_profile.user = user
            employee_profile.curriculum = curriculum_file
            employee_profile.save()
            
            messages.success(request, "Registration successful!")

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
        return render(request, 'error.html', {'message': 'No tienes permisos para acceder a esta oferta'})
    
    applicants = offer.job_applications.select_related('employee').all()

    filter_form = EmployeeFilterForm(request.GET or None)
    if filter_form.is_valid():
        applicants = filter_form.filter_queryset(applicants)

    context = {'applicants': applicants, 'offer': offer, 'filter_form': filter_form}
    return render(request, "applicants_list.html", context)



@login_required
def employee_offer_list(request):
    context = {}

    current_user = request.user
    offers = Offer.objects.all()
    
    try:
        employee = Employee.objects.get(user=current_user)
    except Employee.DoesNotExist:
        return render(request, 'error_employee.html')
    
    search = ''
    offers = Offer.objects.all()
    if request.method == 'POST':
        search = request.POST.get("search", "") 
        if search:
            offers = Offer.objects.filter(Q(title__icontains=search))
        
    applications = {offer.id: offer.job_applications.filter(employee=employee).exists() for offer in offers}
    hirings = {offer.id: EmployeeWorkService.objects.filter(employee=employee, cateringservice=offer.cateringservice).exists() for offer in offers}
    context = {'offers': offers, 'applications': applications, 'search':search, 'hirings': hirings}
    
    return render(request, "employee_offer_list.html", context)

@login_required
def application_to_offer(request, offer_id):
    
    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
    except Employee.DoesNotExist:
        return render(request, 'error_employee.html')

    offer = get_object_or_404(Offer, id=offer_id)
    
    if JobApplication.objects.filter(employee=employee, offer=offer) or EmployeeWorkService.objects.filter(employee=employee, offer=offer):
        return render(request, 'error_employee_already_applied.html')
    elif not employee.curriculum:
        return render(request, 'error_employee_curriculum.html')
    else:
        JobApplication.objects.create(employee=employee, offer=offer, state='PENDING')
        return render(request, "application_success.html")

@login_required
def employee_applications_list(request):

    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
    except Employee.DoesNotExist:
        return render(request, 'error_employee.html')
    
    applications = JobApplication.objects.filter(employee=employee)
    context = {'applications': applications}
    
    return render(request, "application_employee_list.html", context)

@login_required
def my_recommendation_letters(request, employee_id):
    user = request.user
    try:
        employee = Employee.objects.get(user=user)
        if employee.user.id != employee_id:
            return HttpResponseForbidden("You are not allowed to access this.")
    except Employee.DoesNotExist:
        return HttpResponseForbidden("You are not allowed to access this.")
        
    recommendations = RecommendationLetter.objects.filter(employee_id=employee_id)
    
    recommendation_dict = {}
    for recommendation in recommendations:
        catering_company = CateringCompany.objects.get(user_id=recommendation.catering_id)
        recommendation_dict[recommendation] = catering_company
    
    context = {'recommendation_dict': recommendation_dict}

    return render(request, "my_recommendation_letters.html", context)

def listar_caterings_companies(request):
    context = {}
    context["is_particular"] = is_particular(request)
    context["is_employee"] = is_employee(request)
    context["is_catering_company"] = is_catering_company(request)
    if not is_employee(request):
        return HttpResponseForbidden("You are not an employee")
    caterings = CateringCompany.objects.all()

    context["caterings"] = caterings
    return render(request, "contact_chat_employee.html", context)