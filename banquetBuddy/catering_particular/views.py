from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from core.models import CateringService
from core.views import *

def listar_caterings(request):
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)

def catering_detail(request, catering_id):
    context = {}
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)
