from django.shortcuts import render, redirect
from django.contrib import messages

from catering_owners.models import Offer
from .forms import EmployeeFilterForm, EmployeeForm

from core.forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_employee(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():

            user = user_form.save()

            employee_profile = employee_form.save(commit=False)
            employee_profile.user = user
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
