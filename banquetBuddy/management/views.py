from django.shortcuts import render, get_object_or_404
from core.models import Event,BookingState,CateringService
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden


# Create your views here.

@login_required
def confirm_reservation(request, catering_service_id, event_id):
    catering_service = get_object_or_404(CateringService, pk=catering_service_id)
    
    if request.user == catering_service.cateringcompany.user:    
        event = get_object_or_404(Event, pk=event_id)
        event.booking_state = BookingState.CONFIRMED
        event.save()
        return HttpResponse("Reservation confirmed successfully.")
    else:
        return HttpResponseForbidden("You don't have permission to confirm this reservation.")

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


