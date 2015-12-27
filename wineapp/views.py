from django.shortcuts import render

from .models import Wine, Review


def index(request):
    context = {}
    return render(request, 'wineapp/index.html', context)
