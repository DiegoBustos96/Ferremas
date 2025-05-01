# ferremas/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=puedes_cambiar_esta_llave_secreta!&b' # Cambia esto por una llave segura

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Cambia a False para producción

ALLOWED_HOSTS = [] # Agrega los dominios permitidos en producción

CART_SESSION_ID = 'cart' 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Necesario para sesiones (carrito)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ferremas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Agrega la ruta al directorio de plantillas principal
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart', # Agregaremos esto para el carrito global
            ],
        },
    },
]

WSGI_APPLICATION = 'ferremas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # ... (validadores por defecto) ...
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'es-cl' # Español Chile

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/'

# Directorio donde `collectstatic` reunirá los archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directorios adicionales donde Django buscará archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (User uploaded files, like product images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Crea este directorio 'media' en la raíz


# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs para login/logout (si no usas las de admin)
LOGIN_REDIRECT_URL = '/' # A dónde ir después del login
LOGOUT_REDIRECT_URL = '/' # A dónde ir después del logout
LOGIN_URL = 'login'     # Nombre de la URL de login