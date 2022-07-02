import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-94o*g+8_#yhg(j(p6h=2^1l7x_mfad@hj)+f!m%f+9e(w@9po-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CART_SESSION_ID = 'cart'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = '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'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'lesyak2008@ukr.net'
EMAIL_USE_TLS = True

account_sid = 'ACba3baf85b063f2614c78765409b68bb8'
auth_token = '09640e35be5882c9853ad9f155cf0141'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



STATICFILES_DIRS = (
    '/home/userpasha/GraduateProject/sto-kolischa/shop/static',
)

