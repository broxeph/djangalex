from django.shortcuts import render

from .models import Box


def index(request):
    boxes = Box.objects.all()
    context = {'boxes': boxes}
    return render(request, 'home/index.html', context)
