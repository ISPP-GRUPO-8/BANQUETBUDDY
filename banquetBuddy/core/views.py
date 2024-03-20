from django.shortcuts import render, redirect
from catering_employees.models import Employee
from catering_particular.models import Particular

from catering_owners.models import CateringCompany
from .forms import EmailAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from catering_owners.models import  CateringService, Offer
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import sample

def get_user_type(user):
    if hasattr(user, 'ParticularUsername'):
        return "Particular"
    elif hasattr(user, 'CateringCompanyusername'):
        return "Catering Company"
    elif hasattr(user, 'EmployeeUsername'):
        return "Employee"
    else:
        return "Unknown"
      
def home(request):
    context={}
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    return render(request, "core/home.html", context)

def is_particular(request):
    try:
        particular = Particular.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res
    

def is_employee(request):
    try:
        employee = Employee.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res
    

def is_catering_company(request):
    try:
        catering_company = CateringCompany.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res

def home(request):

    context = {}

    offers = Offer.objects.all()  
    random_offers = sample(list(offers), 4)

    caterings = CateringService.objects.all()  
    random_caterings = sample(list(caterings), 4)

    context = {'offers': random_offers, 'caterings': random_caterings}


    return render(request, "core/home.html", context)   

def is_particular(request):
    try:
        particular = Particular.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res
    

def is_employee(request):
    try:
        employee = Employee.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res
    

def is_catering_company(request):
    try:
        catering_company = CateringCompany.objects.get(user = request.user)
        res = True
    except:
        res = False
    return res

def about_us(request):
    return render(request, "core/aboutus.html")


def subscription_plans(request):
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
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar a la página de inicio o a otra página deseada
                return redirect("/")
        # Si el formulario no es válido, renderiza el formulario con los errores
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
        print("Catering Company:", catering_company)  # Imprimir información de depuración
    
    return render(request, "core/profile.html", context)


@login_required
def profile_edit_view(request):
    context = {"user": request.user}

    is_employee = hasattr(request.user, 'EmployeeUsername')
    if is_employee:
        employee_instance = Employee.objects.get(user = request.user)
    else:
        employee_instance = None

    if request.method == "POST":
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        # Pasar valores al contexto
        context["email"] = email
        context["username"] = username
        context["first_name"] = first_name
        context["last_name"] = last_name

        # Validaciones
        if not (email and username and first_name and last_name):
            messages.error(request, "Completa todos los campos")
            return render(request, "core/profile_edit.html", context)

        if (
            CustomUser.objects.filter(email=email)
            .exclude(username=request.user.username)
            .exists()
        ):
            messages.error(request, "El correo electrónico ya está en uso")
            return render(request, "core/profile_edit.html", context)

        if (
            CustomUser.objects.filter(username=username)
            .exclude(username=request.user.username)
            .exists()
        ):
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, "core/profile_edit.html", context)

        if is_employee:
            curriculum_file = request.FILES.get("curriculum")
            if curriculum_file:
                if not curriculum_file.name.endswith('.pdf'):
                    messages.error(request, "Por favor, carga solo archivos PDF")
                    return render(request, "core/profile_edit.html", context)
                if employee_instance.curriculum:
                    employee_instance.curriculum.delete()
                employee_instance.curriculum = curriculum_file
                employee_instance.save()

        user = request.user
        user.email = email
        user.first_name = first_name
        user.username = username
        user.last_name = last_name
        user.save()

        messages.success(request, "Perfil actualizado correctamente")
        return redirect("profile")

    return render(request, "core/profile_edit.html", context)

def listar_caterings_home(request):
    context = {}
    busqueda = ''
    caterings = CateringService.objects.all()
    busqueda = request.POST.get("buscar", "") 
    if busqueda:
        caterings = CateringService.objects.filter(name__icontains=busqueda)

    context['buscar'] = busqueda    
    context['caterings'] = caterings
    return render(request, 'listar_caterings.html', context)





