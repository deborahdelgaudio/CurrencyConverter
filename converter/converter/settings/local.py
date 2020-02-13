import os
from .base import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '(quuswdl+_eo#b5=*c#$g3+0bxty#y(xe(@@vp0)4s^p$@l(x_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DJANGO_DATABASES_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}