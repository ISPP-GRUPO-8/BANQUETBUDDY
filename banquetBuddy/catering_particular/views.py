from django.shortcuts import render, get_object_or_404
from core.models import BookingState, Event, Menu, CateringService
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def my_books(request):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    return render(request, 'my_books.html', context)

@login_required
def book_cancel(request, event_id):
    user = request.user
    events = Event.objects.filter(particular_id = user.id)
    context = {'events': events}
    event = get_object_or_404(Event, id = event_id)
    if user.id == event.particular_id:
        event.booking_state = BookingState.CANCELLED
        event.save()
    return render(request, 'my_books.html', context)

@login_required
def book_edit(request, event_id):
    context = {}
    event = get_object_or_404(Event, id = event_id)
    events = Event.objects.filter(particular_id = request.user.id)
    catering = get_object_or_404(CateringService, id = event.cateringservice_id)
    menus = Menu.objects.filter(cateringservice_id = catering.id)
    context["menus"] = menus
    context["event"] = event

    if request.method == "POST":
        date = request.POST.get("date", "")
        number_guests = request.POST.get("number_guests", "")
        menu = request.POST.get("menu", "")

        context["date"] = date
        context["number_guests"] = number_guests
        context["menu"] = menu
        context["events"] = events

        event.date = date
        event.number_guests = number_guests
        event.menu = menu
        event.booking_state = BookingState.CONTRACT_PENDING
        event.details = f'Reservation for {number_guests} guests'
        event.save()

        return render(request, 'my_books.html', context)

    return render(request, 'book_edit.html', context)
