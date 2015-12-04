DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_3-)v^qk(h5ljg4u@xb@19ju*&1m_r*p*(f%-u+)4e3yjh0&k)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alexball',
        'USER': 'alexball',
        'PASSWORD': 'sudormrf',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
