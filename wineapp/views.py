from django.shortcuts import get_object_or_404, render

from .models import Wine, Review


def index(request):
    context = {}
    return render(request, 'wineapp/index.html', context)


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'wineapp/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'wineapp/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    return render(request, 'wineapp/wine_list.html', {'wine_list': wine_list})


def wine_detail(request, wine_id):
    wine = get_object_or_404(Review, pk=wine_id)
    return render(request, 'wineapp/wine_detail.html', {'wine': wine})
