from django.shortcuts import render

from core.models import CateringService


def listar_caterings(request):
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)