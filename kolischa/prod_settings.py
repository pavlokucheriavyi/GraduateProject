import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

CART_SESSION_ID = 'cart'

ALLOWED_HOSTS = ['.vercel.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kolischa',
        'USER': 'userdb',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = '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'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'kobra1903@ukr.net'
EMAIL_USE_TLS = True

account_sid = 'ACba3baf85b063f2614c78765409b68bb8'
auth_token = '09640e35be5882c9853ad9f155cf0141'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-94o*g+8_#yhg(sdgsdg&324sfdg^mnx)+f!m%f+9e(w@9po-'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_DIRS = (
#     '/home/userpasha/GraduateProject/sto-kolischa/shop/static',
# )
