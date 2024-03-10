from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

from core.models import BookingState, CateringService, Event, Particular, Menu


def listar_caterings(request):
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)

def catering_detail(request, catering_id):
    context = {}
    user = request.user
    particular = Particular.objects.filter(user_id = user.id).exists()
    print(particular)
    context['particular'] = particular
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)

@login_required
def booking_process(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)
    user = request.user
    particular = get_object_or_404(Particular, user_id=user.id)

    eventos = Event.objects.filter(cateringservice_id = catering.id)
    highlighted_dates = []
    

    for evento in eventos:
        highlighted_dates.append(evento.date)
    # Obtener el menú para el catering actual
    highlighted_dates_str = [date.strftime('%Y-%m-%d') for date in highlighted_dates]
    print(highlighted_dates)
    

    menus = Menu.objects.filter(cateringservice_id=catering.id)

    # Coloca el menú dentro del contexto correctamente
    context = {'catering': catering, 'menus': menus,'dates' : highlighted_dates_str}
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        number_guests = request.POST.get('number_guests')

        # Validación y lógica de reserva aquí
        if not (event_date and number_guests):
            messages.error(request, 'Please complete all fields')
            context['form_error'] = True  # Agregar marcador para mostrar mensajes de error

        if int(number_guests) > catering.capacity:
            messages.error(request, 'Number of guests exceeds the catering capacity')
            context['form_error_capacity'] = True

        # Validar que la fecha no esté en el pasado y sea al menos un día en el futuro
        today = datetime.now().date()
        selected_date = datetime.strptime(event_date, '%Y-%m-%d').date()

        if selected_date < today:
            messages.error(request, 'The event date cannot be in the past')
            context['form_error_date'] = True
        elif selected_date == today:
            messages.error(request, 'Reservations must be made at least one day before the event')
            context['form_error_date'] = True

        if Event.objects.filter(cateringservice=catering, date=event_date).exists():
            messages.error(request, 'The selected date is already booked')
            context['form_error_date_selected'] = True

        # Verificar si hay errores en el formulario y, si los hay, volver a renderizar la página con los errores
        if any(key in context for key in ['form_error', 'form_error_capacity', 'form_error_date','form_error_date_selected']):
            return render(request, 'booking_process.html', context)

        # Crear el evento y hacer la reserva
        event = Event.objects.create(
            cateringservice=catering,
            particular=particular,
            name=f'Reservation for {catering.name} by {user.username}',
            date=event_date,
            details=f'Reservation for {number_guests} guests',
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=number_guests
        )

        # Puedes agregar más lógica según sea necesario

        return HttpResponse(f'Reservation confirmed for {catering.name} by {user.username}, on {event_date} with {number_guests} guests.')

    # Si no es una solicitud POST, renderizar la página con el formulario
    return render(request, 'booking_process.html', context)


