from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from core.models import CateringService
from core.views import *
from django.db.models import Q

def listar_caterings(request):
    context = {}
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    caterings = CateringService.objects.all()
    if 'buscar' not in context:
        busqueda = ''

    if request.method == 'POST':
        busqueda = request.POST.get('buscar', '')
        caterings = CateringService.objects.filter(Q(name__icontains=busqueda))
        print(caterings)
        
    context['buscar'] = busqueda    
    context['caterings'] = caterings
    return render(request, 'listar_caterings.html', context)


def catering_detail(request, catering_id):
    context = {}
    context['is_particular'] = is_particular(request)
    context['is_employee'] = is_employee(request)
    context['is_catering_company'] = is_catering_company(request)
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)
