from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from core.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .forms import EmployeeFilterForm

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
    if request.user == catering_service.cateringcompany.user:  
        catering_service = get_object_or_404(CateringService, pk=catering_service_id)
        reservations = catering_service.events.all()
        return render(request,'reservations.html',{'reservations': reservations,'catering_service':catering_service})
    else:
        return HttpResponseForbidden("You don't have permission to view this reservations.")
    
@login_required
def view_reservation(request, event_id,catering_service_id):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    if request.user == catering_service.cateringcompany.user:  
        event = get_object_or_404(Event, pk=event_id)
        return render(request,'view_reservation.html',{'event': event})
    else:
        return HttpResponseForbidden("You don't have permission to view this reservation.")
