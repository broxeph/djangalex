from random import randint

from django.shortcuts import render

from .models import Box, Quote


def index(request):
    def get_random_item(model):
        """Return a random item from any model"""
        count = model.objects.all().count()
        return model.objects.all()[randint(0, count - 1)]

    boxes = Box.objects.all().order_by('sort_order')
    quote = get_random_item(Quote)
    context = {'boxes': boxes, 'quote': quote}
    return render(request, 'home/index.html', context)
