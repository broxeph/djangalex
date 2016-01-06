import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
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


@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = Review()
        review.wine = wine
        review.user_name = request.user.username
        review.rating = form.cleaned_data['rating']
        review.comment = form.cleaned_data['comment']
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(
            reverse('wineapp:wine_detail', args=(wine.id,)))

    return render(
        request, 'wineapp/wine_detail.html', {'wine': wine, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(
        user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'wineapp/user_review_list.html', context)
