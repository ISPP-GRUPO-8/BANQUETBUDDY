from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from core.models import CateringService, Particular, Review


def listar_caterings(request):
    caterings = CateringService.objects.all()
    context = {'caterings': caterings}
    return render(request, 'listar_caterings.html', context)

def catering_detail(request, catering_id):
    context = {}
    catering = get_object_or_404(CateringService, id=catering_id)
    context['catering'] = catering

    reviews_list = Review.objects.filter(cateringservice_id=catering.id).order_by('-date')
    
    paginator = Paginator(reviews_list, 3)  # Muestra 3 reviews por página
    page = request.GET.get('page')

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    context['reviews'] = reviews

    user = request.user
    particular = Particular.objects.filter(user_id=user.id)
    context['particular'] = particular

    return render(request, 'catering_detail.html', context)

def catering_review(request, catering_id):
    catering = get_object_or_404(CateringService, id=catering_id)
    user = request.user
    particular = Particular.objects.filter(user_id=user.id)

    if particular:
        context = {'catering': catering, 'particular':particular}

        if request.method == 'POST':
            description = request.POST.get('description')
            rating = request.POST.get('rating')

            review = Review.objects.create(
                cateringservice=catering,
                particular=Particular.objects.get(user=user),
                date=datetime.now().date(),
                description=description,
                rating=rating
            )

            url_catering = reverse('catering_detail', args=[catering.id])
            return redirect(url_catering)
    else:
        return redirect("/")

    return render(request, 'catering_review.html', context)



