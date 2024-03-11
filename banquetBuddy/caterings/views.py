from django.shortcuts import render, get_object_or_404, redirect
from core.models import CateringService, CateringCompany
from django.contrib import messages


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

    # Validar los filtros de precio máximo y número de invitados
    if precio_maximo:
        if not precio_maximo.isdigit() or int(precio_maximo) < 0:
            messages.error(request, "El precio máximo debe ser un número.")
            precio_maximo = ""

    if num_invitados:
        if not num_invitados.isdigit() or int(num_invitados) < 0:
            messages.error(request, "El número de invitados debe ser un número.")
            num_invitados = ""

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

    return render(request, "listar_caterings.html", context)


def catering_detail(request, catering_id):
    context = {}
    catering = get_object_or_404(CateringService, id=catering_id)
    context["catering"] = catering
    return render(request, "catering_detail.html", context)
