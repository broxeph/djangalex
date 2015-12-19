from django.shortcuts import render

from .models import Box


def index(request):
    boxes = Box.objects.all().order_by('sort_order')
    context = {'boxes': boxes}
    return render(request, 'home/index.html', context)
