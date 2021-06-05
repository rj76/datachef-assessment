from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datachef',
        'USER': 'datachef',
        'PASSWORD': 'datachef',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
