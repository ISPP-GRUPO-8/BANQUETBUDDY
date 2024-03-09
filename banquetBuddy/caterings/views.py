from django.shortcuts import render, redirect
from core.models import CateringService, CateringCompany


def listar_caterings(request):
    caterings = CateringService.objects.all()

    # Obtener tipos de cocina únicos
    tipos_cocina = (
        CateringCompany.objects.values_list("cuisine_type", flat=True)
        .exclude(cuisine_type__isnull=True)
        .distinct()
    )
    tipos_cocina = [str(tipo[0]) for tipo in tipos_cocina if tipo[0]]

    # Obtener los parámetros de filtrado de la solicitud GET
    cocina = request.GET.get("cocina", "")
    precio_maximo = request.GET.get("precio_maximo", "")
    num_invitados = request.GET.get("num_invitados", "")

    # Verificar si se ha enviado algún botón de "eliminar filtro"
    limpiar_cocina = request.GET.get("limpiar_cocina", None)
    limpiar_precio = request.GET.get("limpiar_precio", None)
    limpiar_invitados = request.GET.get("limpiar_invitados", None)

    # Aplicar los filtros si se proporcionan
    if cocina and not limpiar_cocina:
        caterings = caterings.filter(cateringcompany__cuisine_type__icontains=cocina)
    else:
        cocina = ""
    if precio_maximo and not limpiar_precio:
        caterings = caterings.filter(price__lte=precio_maximo)
    else:
        precio_maximo = ""
    if num_invitados and not limpiar_invitados:
        caterings = caterings.filter(capacity__gte=num_invitados)
    else:
        num_invitados = ""

    context = {
        "caterings": caterings,
        "tipos_cocina": tipos_cocina,
        "cocina": cocina,
        "precio_maximo": precio_maximo,
        "num_invitados": num_invitados,
    }

    print(tipos_cocina)
    return render(request, "listar_caterings.html", context)
