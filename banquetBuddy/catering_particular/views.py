from django.shortcuts import render, get_object_or_404
from core.models import CateringService, CateringCompany
from django.contrib import messages
from django.http import HttpResponseForbidden
from core.views import *


def obtener_filtros(request):
    filtros = {
        "cocina": request.GET.get("cocina", ""),
        "precio_maximo": request.GET.get("precio_maximo", ""),
        "num_invitados": request.GET.get("num_invitados", ""),
    }

    limpiar_filtros = {
        "limpiar_cocina": request.GET.get("limpiar_cocina", None),
        "limpiar_precio": request.GET.get("limpiar_precio", None),
        "limpiar_invitados": request.GET.get("limpiar_invitados", None),
    }

    return filtros, limpiar_filtros


def validar_filtros(request, filtros):
    if filtros["precio_maximo"]:
        if not filtros["precio_maximo"].isdigit() or int(filtros["precio_maximo"]) < 0:
            messages.error(request, "El precio máximo debe ser un número positivo.")
            filtros["precio_maximo"] = ""

    if filtros["num_invitados"]:
        if not filtros["num_invitados"].isdigit() or int(filtros["num_invitados"]) < 0:
            messages.error(
                request, "El número de invitados debe ser un número positivo."
            )
            filtros["num_invitados"] = ""

    return filtros


def aplicar_filtros(caterings, filtros, limpiar_filtros):
    if filtros["cocina"] and not limpiar_filtros["limpiar_cocina"]:
        caterings = caterings.filter(
            cateringcompany__cuisine_types__type=filtros["cocina"]
        )
    else:
        filtros["cocina"] = ""
    if filtros["precio_maximo"] and not limpiar_filtros["limpiar_precio"]:
        caterings = caterings.filter(price__lte=filtros["precio_maximo"])
    else:
        filtros["precio_maximo"] = ""
    if filtros["num_invitados"] and not limpiar_filtros["limpiar_invitados"]:
        caterings = caterings.filter(capacity__gte=filtros["num_invitados"])
    else:
        filtros["num_invitados"] = ""

    return caterings, filtros


def listar_caterings(request):
  
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    caterings = CateringService.objects.all()

    # Obtener tipos de cocina únicos
    tipos_cocina = (
        CateringCompany.objects.values_list("cuisine_types__type", flat=True)
        .exclude(cuisine_types__isnull=True)
        .distinct()
    )
    print(tipos_cocina)

    filtros, limpiar_filtros = obtener_filtros(request)
    filtros = validar_filtros(request, filtros)
    caterings, filtros = aplicar_filtros(caterings, filtros, limpiar_filtros)

    context = {
        "caterings": caterings,
        "tipos_cocina": tipos_cocina,
        **filtros,
    }

    return render(request, "listar_caterings.html", context)


def catering_detail(request, catering_id):
    context = {}
    if not is_particular(request):
        return HttpResponseForbidden("No eres cliente")
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)

