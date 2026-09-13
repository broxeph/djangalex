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
