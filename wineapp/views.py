import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Wine, Review
from .forms import ReviewForm


def index(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
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
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(
        request, 'wineapp/wine_detail.html', {'wine': wine, 'form': form})


def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = Review()
        review.wine = wine
        review.user_name = form.cleaned_data['user_name']
        review.rating = form.cleaned_data['rating']
        review.comment = form.cleaned_data['comment']
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(
            reverse('wineapp:wine_detail', args=(wine.id,)))

    return render(
        request, 'wineapp/wine_detail.html', {'wine': wine, 'form': form})
