import os
from django.contrib import messages # To change ERROR into Danger

# import environ # To use .env file

# using python-dotenv
from dotenv import load_dotenv
load_dotenv()


from pathlib import Path
from mongoengine import connect

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=$!k4_-j55pd3i5ku^0$%h%wp^q)6^#xva$gvf(4*ce)i*99mv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'apps.courses',
    'apps.core',
    'apps.users',

    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'courseproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.courses.context_processors.head_menu',
                'apps.courses.context_processors.my_courses',
            ],
        },
    },
]

# For Django All Auth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'courseproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Database - MongoDB configuration using Djongo
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'coursedb',
        'ENFORCE_SCHEMA_VALIDATION': False,
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}
'''



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coursedb',          # Make sure you created this in MySQL!
        'USER': 'root',              # Your MySQL username
        'PASSWORD': 'root',  # Your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# Local static assets live in the top-level "static" folder
STATICFILES_DIRS = [BASE_DIR / 'static']
# Collected static files for production (e.g., via collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Settings for Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For Red Color on Error MEssages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Using .env

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')




# For Django All Auth
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# Modern Allauth settings (django-allauth >= 0.63.0)
# Replaces deprecated ACCOUNT_AUTHENTICATION_METHOD and ACCOUNT_EMAIL_REQUIRED
ACCOUNT_LOGIN_METHODS = {'email'}  # Login via email only
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# Security settings
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

# Rate limiting (replaces deprecated ACCOUNT_LOGIN_ATTEMPTS_LIMIT/TIMEOUT)
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m',  # 5 attempts per 5 minutes
}

# Email verification (set to 'mandatory' for production)
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}