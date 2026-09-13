from django.conf import settings
from storages.backends.s3 import S3Storage
from whitenoise.storage import CompressedManifestStaticFilesStorage


class StaticStorage(CompressedManifestStaticFilesStorage):
    """Hashed, precompressed static files served by WhiteNoise.

    Home page logo paths come from the database, so a missing file falls back to
    its plain URL (a broken image) instead of raising and taking the page down.
    """

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            return name


class MediaStorage(S3Storage):
    """Upload to 'mybucket/media/', serve from 'cloudfront.net/media/'."""
    location = settings.MEDIA_LOCATION

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)
