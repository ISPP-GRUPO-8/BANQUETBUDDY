from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from core.models import BookingState, CateringService, Event, Particular


def listar_caterings(request):
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)

def catering_detail(request, catering_id):
    context = {}
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)

@login_required
def booking_process(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)
    user = request.user
    particular = get_object_or_404(Particular, user_id=user.id)
    context = {'catering': catering}

    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        number_guests = request.POST.get('number_guests')

        # Validation and booking logic here
        if not (event_date and number_guests):
            messages.error(request, 'Please complete all fields')
            context['form_error'] = True  # Add marker to show error messages

        if int(number_guests) > catering.capacity:
            messages.error(request, 'Number of guests exceeds the catering capacity')
            context['form_error_capacity'] = True

        # Validate that the date is not in the past and is at least one day in the future
        today = datetime.now().date()
        selected_date = datetime.strptime(event_date, '%Y-%m-%d').date()

        if selected_date < today:
            messages.error(request, 'The event date cannot be in the past')
            context['form_error_date'] = True
        elif selected_date == today:
            messages.error(request, 'Reservations must be made at least one day before the event')
            context['form_error_date'] = True

        if 'form_error' or 'form_error_capacity' or 'form_error_date' in context:
            return render(request, 'booking_process.html', context)

        # Create the event and make the reservation
        event = Event.objects.create(
            cateringservice=catering,
            particular=particular,
            name=f'Reservation for {catering.name} by {user.username}',
            date=event_date,
            details=f'Reservation for {number_guests} guests',
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=number_guests
        )

        # You can add more logic as needed

        return HttpResponse(f'Reservation confirmed for {catering.name} by {user.username}, on {event_date} with {number_guests} guests.')

    # If it's not a POST request, render the page with the form
    return render(request, 'booking_process.html', context)

