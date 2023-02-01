"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os   # logging 에서 사용

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zz&n$q*_5494ap^^&o#=aw8&r#%b6*ua9x2ez^pq^nzljku+33'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
#ALLOWED_HOSTS = ["127.0.0.1",'192.168.0.']


# Application definition

INSTALLED_APPS = [
    'pybo.apps.PyboConfig',  # /Users/ckair/projects/mysite/pybo/apps.py
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],                 # BASE_DIR/templates == projects/mysite/templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
	    'version': 1,
	    'disable_existing_loggers': False,
	    'filters': {
	        'require_debug_false': {
	            '()': 'django.utils.log.RequireDebugFalse',
	        },
	        'require_debug_true': {
	            '()': 'django.utils.log.RequireDebugTrue',
	        },
	    },
	    # 형식정의
	    'formatters': {
	        'format1': {'format': '[%(asctime)s] %(module)s -%(lineno)d %(levelname)s %(message)s','datefmt': "%Y-%m-%d %H:%M:%S"},
	        'format2': {'format': '%(levelname)s %(message)s [%(name)s:%(lineno)s]'},
	    },
	    'handlers': {
	        # 파일저장
	        'file': {
	                'level': 'INFO',
	                'class': 'logging.handlers.RotatingFileHandler',
	                'filename': os.path.join(BASE_DIR, 'logs/python_pybo.log'),
	                'encoding': 'UTF-8',
	                'maxBytes': 1024 * 1024 * 5,  # 5 MB
	                'backupCount': 5,
	                'formatter': 'format1',
	                },
	        # 콘솔(터미널)에 출력
	        'console': {
	            'level': 'INFO',
	            'filters': ['require_debug_true'],
	            'class': 'logging.StreamHandler',
                'formatter': 'format1',
	        },
	    },
	    'loggers': {
	        #종류
	        'django.server': {
	            'handlers': ['file','console'],
	            'propagate': False,
	            'level': 'DEBUG',
	        },
	        'django.request': {
	            'handlers':['file','console'],
	            'propagate': False,
	            'level':'DEBUG',
	        },
	        '': {
	            'level': 'DEBUG',
	            'handlers': ['file','console'],
	            'propagate': True,
	        },
	    },
	}
















