from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import (
    ParticularForm,
    CateringCompanyForm,
    EmployeeForm,
    CustomUserCreationForm,
    OfferForm
)
from django.contrib import messages
from .models import CustomUser, Offer, CateringCompany, CateringService
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "core/home.html")


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


def register_particular(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        particular_form = ParticularForm(request.POST)

        if user_form.is_valid() and particular_form.is_valid():

            user = user_form.save()

            particular_profile = particular_form.save(commit=False)
            particular_profile.user = user
            particular_profile.save()
            messages.success(request, "Registration successful!")

            return redirect("home")

    else:
        user_form = CustomUserCreationForm()
        particular_form = ParticularForm()

    return render(
        request,
        "core/registro_particular.html",
        {"user_form": user_form, "particular_form": particular_form},
    )


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


def register_company(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        company_form = CateringCompanyForm(request.POST)

        if user_form.is_valid() and company_form.is_valid():

            user = user_form.save()

            company_profile = company_form.save(commit=False)
            company_profile.user = user
            company_profile.save()
            messages.success(request, "Registration successful!")

            return redirect("home")

    else:
        user_form = CustomUserCreationForm()
        company_form = CateringCompanyForm()

    return render(
        request,
        "core/registro_company.html",
        {"user_form": user_form, "company_form": company_form},
    )


def elegir_registro(request):
    return render(request, "core/elegir_registro.html")


@login_required
def profile_view(request):
    context = {}
    context["user"] = request.user
    return render(request, "core/profile.html", context)


@login_required
def profile_edit_view(request):
    context = {}
    context["user"] = request.user

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

        user = request.user
        user.email = email
        user.first_name = first_name
        user.username = username
        user.last_name = last_name

        user.save()

        return redirect("profile")

    return render(request, "core/profile_edit.html", context)

def offer_list(request):
    offers = Offer.objects.all() 
    return render(request, 'core/offer_list.html', {'offers': offers})

@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            catering_company = request.user.CateringCompanyusername
            catering_service = get_object_or_404(CateringService, cateringcompany=catering_company)
            offer = form.save(commit=False)
            offer.cateringservice = catering_service
            offer.save()
            return redirect('offer_list')
    else:
        form = OfferForm()
    
    return render(request, 'core/create_offer.html', {'form': form})

def edit_offer(request, offer_id): 
    offer = get_object_or_404(Offer, pk=offer_id) 
    if request.user == offer.cateringservice.cateringcompany.user:
        if request.method == 'POST':
            form = OfferForm(request.POST, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = OfferForm(instance=offer)
        return render(request, 'edit_offer.html', {'form': form})
    else:
        return redirect('home')  

@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user == offer.cateringservice.cateringcompany.user:
        if request.method == 'POST':
            offer.delete()
            return redirect('home') 
        return render(request, 'delete_offer.html', {'offer': offer})
    else:
        return redirect('home')
    
def apply_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Procesar la aplicación, por ejemplo, guardarla en la base de datos
            application = form.save(commit=False)
            application.offer = offer  # Asignar la oferta a la aplicación
            application.save()
            # Aquí podrías agregar cualquier lógica adicional, como enviar un correo electrónico de confirmación
            return redirect('offer_list')  # Redirigir de vuelta a la lista de ofertas después de aplicar
    else:
        form = OfferForm()

    return render(request, 'offer_list.html', {'form': form, 'offer': offer})