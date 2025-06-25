import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS =config('ALLOWED_HOSTS',default='108.181.155.189', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Packages tiers
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    'phonenumber_field',
    
    # Vos apps
    'core.apps.CoreConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cashprint_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'cashprint_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
#         'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
#         'USER': config('DB_USER', default=''),
#         'PASSWORD': config('DB_PASSWORD', default=''),
#         'HOST': config('DB_HOST', default=''),
#         'PORT': config('DB_PORT', default=''),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Phone Number Field Configuration
PHONENUMBER_DEFAULT_REGION = 'CM'  # Cameroun

# Authentication Configuration
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cashprint.cm')

# Security Settings (Production)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'cashprint.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },}

# Session Configuration
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Cash Print Specific Settings
CASHPRINT_SETTINGS = {
    'STUDENT_DISCOUNT': config('STUDENT_DISCOUNT', default=0.20, cast=float),
    'QUANTITY_DISCOUNTS': {
        50: 0.05,   # 5% pour 50+
        100: 0.10,  # 10% pour 100+
        250: 0.15,  # 15% pour 250+
        500: 0.20,  # 20% pour 500+
    },
    'DEFAULT_CURRENCY': config('DEFAULT_CURRENCY'),
    'CURRENCY_SYMBOL': config('CURRENCY_SYMBOL'),
    'COMPANY_NAME': config('COMPANY_NAME'),
    'COMPANY_ADDRESS': config('COMPANY_ADDRESS'),
    'COMPANY_PHONE': config('COMPANY_PHONE'),
    'COMPANY_EMAIL': config('COMPANY_EMAIL'),
    'COMPANY_WEBSITE': config('COMPANY_WEBSITE'),

    # Limites et contraintes
    'MIN_ORDER_AMOUNT': config('MIN_ORDER_AMOUNT', default=500, cast=int),
    'MAX_ORDER_AMOUNT': config('MAX_ORDER_AMOUNT', default=500000, cast=int),
    'MIN_CREDIT_RECHARGE': config('MIN_CREDIT_RECHARGE', default=1000, cast=int),
    'MAX_CREDIT_RECHARGE': config('MAX_CREDIT_RECHARGE', default=100000, cast=int),
    'MAX_FILE_SIZE_MB': config('MAX_FILE_SIZE_MB', default=10, cast=int),
    
    # Paramètres d'impression
    'SUPPORTED_FILE_TYPES': ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'],
    'MAX_PAGES_PER_ORDER': config('MAX_PAGES_PER_ORDER', default=1000, cast=int),
    'DEFAULT_PROCESSING_TIME_MINUTES': config('DEFAULT_PROCESSING_TIME_MINUTES', default=30, cast=int),
    
    # Paramètres de notification
    'SEND_SMS_NOTIFICATIONS': config('SEND_SMS_NOTIFICATIONS', default=False, cast=bool),
    'SEND_EMAIL_NOTIFICATIONS': config('SEND_EMAIL_NOTIFICATIONS', default=True, cast=bool),
    
    # Mode maintenance
    'MAINTENANCE_MODE': config('MAINTENANCE_MODE', default=False, cast=bool),
    'MAINTENANCE_MESSAGE': config('MAINTENANCE_MESSAGE', default='Site en maintenance. Merci de revenir plus tard.'),
}

# Cache Configuration (pour la production)
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Celery Configuration (pour les tâches asynchrones - optionnel)
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Création automatique du dossier logs
os.makedirs(BASE_DIR / 'logs', exist_ok=True)