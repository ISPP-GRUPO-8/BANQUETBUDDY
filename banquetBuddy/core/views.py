from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from catering_employees.models import Employee
from catering_particular.models import Particular

from catering_owners.models import CateringCompany
from .forms import EmailAuthenticationForm, CustomUserCreationForm

from catering_particular.forms import ParticularForm
from catering_employees.forms import EmployeeForm
from catering_owners.forms import CateringCompanyForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .forms import ErrorForm

from django.contrib import messages
from .models import CustomUser
from catering_owners.models import  CateringService, Offer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import sample
from django.utils import timezone
from datetime import datetime, timedelta
from catering_owners.models import NotificationEvent, NotificationJobApplication
from catering_owners.models import Event


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
    context={}
    offers = Offer.objects.all()  
    random_offers = sample(list(offers), 4)

    caterings = CateringService.objects.all()  
    random_caterings = sample(list(caterings), 4)
    
    if request.user.is_authenticated:
        notifications = NotificationEvent.objects.filter(user=request.user, has_been_read=False).count() + NotificationJobApplication.objects.filter(user=request.user, has_been_read=False).count()
        context['notification_number'] = notifications
    
    context['offers'] = random_offers
    context['caterings'] = random_caterings
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


def about_us(request):
    return render(request, "core/aboutus.html")


def subscription_plans(request):
    if is_catering_company(request):
        catering_company = CateringCompany.objects.get(user=request.user)
        return render(request, "core/subscriptionsplans.html", {"price_plan": catering_company.price_plan})
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
                
                #Comprueba si el usuario es particular o empresa
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

@login_required
def error_report(request):
    if request.method == 'POST':
        form = ErrorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            message = form.cleaned_data['message']
            reporter_email = form.cleaned_data['reporter_email']
            error_type = form.cleaned_data['error_type']
            
            email = 'banquetbuddyoficial@gmail.com'

            client_type = get_user_type(request.user)

            error_type_display = dict(form.fields['error_type'].choices)[error_type]

            contenido_correo = f'Name: {name} {surname} | Client Type: {client_type} | Contact Mail: {reporter_email} | Error type: {error_type_display} | Mensaje: {message}'
            
            subject = 'Error Report'
            message = contenido_correo
            from_email = 'banquetbuddyoficial@gmail.com' 
            to_email = [email] 

            send_mail(subject, message, from_email, to_email, html_message=message)

            return redirect("/")
    else:
        form = ErrorForm()

    return render(request, 'core/error_report.html', {'form': form})

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

def notification_view(request):
    
    current_user = request.user
    try:
        employee = Employee.objects.get(user=current_user)
        notifications = NotificationJobApplication.objects.filter(user=current_user, has_been_read=False)
        for notification in notifications:
            notification.has_been_read = True
            notification.save()
    except Employee.DoesNotExist:
        notifications = NotificationEvent.objects.filter(user=current_user, has_been_read=False)
        for notification in notifications:
            notification.has_been_read = True
            notification.save()
    context = {'notifications' : notifications}
        
    return render(request, 'core/notifications.html', context)

#Notification check functions

def send_notifications_next_events_particular(request):
    current_user = request.user
    NotificationEvent.objects.filter(user=current_user, has_been_read=True).delete()
    week_after = timezone.now() + timedelta(days=7)
    next_events = Event.objects.filter(date__lte=week_after, particular__user=current_user)
    
    for event in next_events:
        
        if not event.notified_to_particular:
            message = f"Your event is prepared for {event.date}. ¡Don't forget to get ready!"
            NotificationEvent.objects.create(user=current_user, message=message, event=event)
            event.notified_to_particular = True
            event.save()
            
def send_notifications_next_events_catering_company(request):
    current_user = request.user
    NotificationEvent.objects.filter(user=current_user, has_been_read=True).delete()
    week_after = timezone.now() + timedelta(days=7)
    catering_company = get_object_or_404(CateringCompany, user=current_user)
    next_events = Event.objects.filter(date__lte=week_after, cateringservice__cateringcompany=catering_company)
    
    for event in next_events:
        
        if not event.notified_to_catering_company:
            message = f"There is an upcoming event on {event.date}. ¡Make sure everything is prepared!"
            NotificationEvent.objects.create(user=current_user, message=message, event=event)
            event.notified_to_catering_company = True
            event.save()


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'core/terms_and_conditions.html')




