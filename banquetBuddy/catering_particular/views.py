from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def catering_contratados(request):
    context = {}
    particular = get_object_or_404(Particular, user=request.user)
    events = Event.objects.filter(particular=particular)
    context['events'] = events
    return render(request, 'catering_contratado.html', context)