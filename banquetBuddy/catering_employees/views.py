from django.shortcuts import render, redirect
from django.contrib import messages

from catering_owners.models import Offer, JobApplication
from .models import Employee
from .forms import EmployeeFilterForm, EmployeeForm

from core.forms import CustomUserCreationForm
from catering_owners.models import JobApplication, Employee
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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

    current_user = request.user
    offers = Offer.objects.all()
    
    try:
        employee = Employee.objects.get(user=current_user)
    except Employee.DoesNotExist:
        return render(request, 'error_employee.html')
    
    applications = {offer.id: offer.job_applications.filter(employee=employee).exists() for offer in offers}
    context = {'offers': offers, 'applications': applications}
    
    return render(request, "employee_offer_list.html", context)

def application_to_offer(request, offer_id):
    
    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
    except Employee.DoesNotExist:
        return render(request, 'error_employee.html')

    offer = get_object_or_404(Offer, id=offer_id)
    
    if JobApplication.objects.filter(employee=employee, offer=offer):
        return render(request, 'error_employee_already_applied.html')
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