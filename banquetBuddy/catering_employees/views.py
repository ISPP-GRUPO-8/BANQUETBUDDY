from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmployeeForm

from core.forms import CustomUserCreationForm

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
