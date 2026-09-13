from django.conf import settings


def analytics(request):
    """Expose the Google Analytics measurement ID (empty when analytics is off)."""
    return {'GA_MEASUREMENT_ID': settings.GA_MEASUREMENT_ID}
