from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime
from core.models import CateringService, Particular, Review


def listar_caterings(request):
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)

def catering_detail(request, catering_id):
    context = {}
    catering = get_object_or_404(CateringService, id = catering_id)
    context['catering'] = catering
    return render(request, 'catering_detail.html', context)

def catering_review(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)
    user = request.user
    particular = get_object_or_404(Particular, user_id=user.id)
    context = {'catering': catering}

    if request.method == 'POST':
        description = request.POST.get('description')
        rating = request.POST.get('rating')

        review = Review.objects.create(
            cateringservice=catering,
            particular=particular,
            date=datetime.now().date(),
            description=description,
            rating=rating
        )

        url_catering = reverse('catering_detail', args=[catering.id])
        return redirect(url_catering)

    return render(request, 'catering_review.html', context)



