from django.shortcuts import render, redirect
from .forms import EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
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
