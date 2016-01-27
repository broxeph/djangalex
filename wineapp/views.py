import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Wine, Review, Post
from .forms import ReviewForm


def index(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    posts = Post.objects.order_by('-pub_date')[:4]
    context = {'latest_review_list': latest_review_list, 'posts': posts}
    return render(request, 'wineapp/index.html', context)


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {
        'latest_review_list': latest_review_list, 'page_title': 'Review list'}
    return render(request, 'wineapp/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    page_title = 'Review detail: ' + review.wine.name
    return render(request, 'wineapp/review_detail.html', {
        'review': review, 'page_title': page_title})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    return render(request, 'wineapp/wine_list.html', {
        'wine_list': wine_list, 'page_title': 'Wine list'})


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    page_title = 'Wine detail: ' + wine.name
    return render(request, 'wineapp/wine_detail.html', {
        'wine': wine, 'form': form, 'page_title': page_title})


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
    page_title = 'User reviews: ' + username
    context = {
        'latest_review_list': latest_review_list, 'username': username,
        'page_title': page_title}
    return render(request, 'wineapp/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    # Get request user reviewed wines and IDs
    user_reviews = Review.objects.filter(
        user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # Get a wine list including the previous IDs, sorted by descending rating
    wine_list = sorted(
        list(Wine.objects.exclude(id__in=user_reviews_wine_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request, 'wineapp/user_recommendation_list.html',
        {'username': request.user.username, 'wine_list': wine_list,
            'page_title': 'Wine recommendations'})
