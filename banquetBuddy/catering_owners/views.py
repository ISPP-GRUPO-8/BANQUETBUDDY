from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OfferForm

from core.models import  Offer, CateringService
from django.contrib.auth.decorators import login_required

# Create your views here.
def offer_list(request):
    offers = Offer.objects.all() 
    return render(request, 'offers/offer_list.html', {'offers': offers})

@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            catering_service = get_object_or_404(CateringService, pk=13)  # Obtiene el CateringService con ID 13
            offer.cateringservice = catering_service
            offer.save()
            return redirect('offer_list')
    else:
        form = OfferForm()
    
    return render(request, 'offers/create_offer.html', {'form': form})

@login_required
def edit_offer(request, offer_id): 
    offer = get_object_or_404(Offer, pk=offer_id) 
    if request.user == offer.cateringservice.cateringcompany.user:
        if request.method == 'POST':
            form = OfferForm(request.POST, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('offer_list')  
        else:
            form = OfferForm(instance=offer)
        return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})
    else:
        return redirect('offer_list')

def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offers/delete_offer.html', {'offer': offer})

@login_required
def confirm_delete_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        offer.delete()
        return redirect('offer_list')
    else:
        return redirect('offer_list')
    
def apply_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Procesar la aplicación, por ejemplo, guardarla en la base de datos
            application = form.save(commit=False)
            application.offer = offer  # Asignar la oferta a la aplicación
            application.save()
            # Aquí podrías agregar cualquier lógica adicional, como enviar un correo electrónico de confirmación
            return redirect('offer_list')  # Redirigir de vuelta a la lista de ofertas después de aplicar
    else:
        form = OfferForm()

    return render(request, 'offers/offer_list.html', {'form': form, 'offer': offer})