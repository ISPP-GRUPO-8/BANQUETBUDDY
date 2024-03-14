from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from core.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from .forms import EmployeeFilterForm
from datetime import datetime
from django.utils.dateformat import DateFormat
import calendar


# Create your views here.

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
def view_reservations(request, catering_service_id):

    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    #if request.user == catering_service.cateringcompany.user:  
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    reservations = catering_service.events.all()
    return render(request,'reservations.html',{'reservations': reservations,'catering_service':catering_service})
    #else:
    #    return HttpResponseForbidden("You don't have permission to view this reservations.")
    
@login_required
def view_reservation(request, event_id,catering_service_id):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:  
        event = get_object_or_404(Event, pk=event_id)
        return render(request,'view_reservation.html',{'event': event})
    else:
        return HttpResponseForbidden("You don't have permission to view this reservation.")


def catering_calendar_view(request, catering_service_id,month,year):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:  
        month = min(max(int(month), 1), 12)  # Asegurarse de que el mes esté en el rango válido (1-12)

        month_name = DateFormat(datetime(year, month, 1)).format('F')

    # Obtener el calendario del mes y los días con eventos
        cal = calendar.monthcalendar(year, month)
        events = Event.objects.filter(
            cateringservice=catering_service,
            date__year=year,
            date__month=month
    ).values_list('date__day', flat=True)

    # Generar una lista de días con eventos para resaltar en el calendario
        event_days = set(events)


        return render(request, 'calendar.html', {
            'catering_name': catering_service.name,
            'catering_service_id':catering_service_id,
            'year': year,
            'month': month,
            'month_name':month_name,
            'cal': cal,
            'event_days': event_days
        })
    else:
        return HttpResponseForbidden("You don't have permission to view this calendar.")

def reservations_for_day(request, catering_service_id, year, month, day):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        selected_date = datetime(year, month, day)
        reservations = Event.objects.filter(cateringservice=catering_service, date=selected_date)
        return render(request, 'reservations_for_day.html', {'catering_service': catering_service,'selected_date': selected_date, 'reservations': reservations})
    else:
        return HttpResponseForbidden("You don't have permission to view this day reservations.")
    

def next_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        next_month = int(month) + 1
        next_year = int(year)
        if next_month > 12:
            next_month = 1
            next_year += 1
    else:
        return HttpResponseForbidden("You don't have permission to manipulate this calendar.")

    return redirect('catering_calendar', catering_service_id=catering_service_id, year=next_year, month=next_month)

def prev_month_view(request, catering_service_id, year, month):
    catering_service = CateringService.objects.get(pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:
        prev_month = int(month) - 1
        prev_year = int(year)
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
    else:
        return HttpResponseForbidden("You don't have permission to manipulate this calendar.")
    
    return redirect('catering_calendar', catering_service_id=catering_service_id, year=prev_year, month=prev_month)

