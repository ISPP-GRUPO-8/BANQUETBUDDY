from django.shortcuts import render
from core.models import CateringService
from django.db.models import Q


def listar_caterings(request):
    context = {}
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

