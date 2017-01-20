from random import randint

from django.shortcuts import render

from .models import Box, Subtitle


def index(request):
    def get_random_item(model):
        """Return a random item from any model."""
        count = model.objects.all().count()
        return model.objects.all()[randint(0, count - 1)] if count else None

    boxes = Box.objects.all().order_by('sort_order')
    subtitle = get_random_item(Subtitle)

    return render(request, 'home/index.html', {'boxes': boxes, 'subtitle': subtitle})
