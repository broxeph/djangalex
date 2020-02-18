from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    """Upload to 'mybucket/static/', serve from 'cloudfront.net/static/'."""
    location = settings.STATIC_LOCATION

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(StaticStorage, self).__init__(*args, **kwargs)


class MediaStorage(S3BotoStorage):
    """Upload to 'mybucket/media/', serve from 'cloudfront.net/media/'."""
    location = settings.MEDIA_LOCATION

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)
