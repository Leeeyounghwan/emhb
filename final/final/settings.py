"""
Django settings for final project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import json, os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open('trip/config.json', 'r') as f:
    json_data = json.load(f)
    secret_key = json_data['SECRET_KEY']
    social_auth_google_oauth2_key = json_data['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
    social_auth_google_oauth2_secret = json_data['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
    social_auth_google_oauth2_redirect_uri = json_data['SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI']
    social_auth_naver_key = json_data['SOCIAL_AUTH_NAVER_KEY']
    social_auth_naver_secret = json_data['SOCIAL_AUTH_NAVER_SECRET']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "trip",
    'daphne',
    'channels',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    
    # allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # allauth - naver
    'allauth.socialaccount.providers.naver',
    'board',    
    'django_summernote',
    'social_django',
    'rest_framework',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = social_auth_google_oauth2_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = social_auth_google_oauth2_secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = social_auth_google_oauth2_redirect_uri

# allauth site_id
SITE_ID = 2

LOGIN_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = reverse_lazy('trip:profile')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.naver.NaverOAuth2',
)

SOCIAL_AUTH_NAVER_KEY= social_auth_naver_key
SOCIAL_AUTH_NAVER_SECRET  = social_auth_naver_secret
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'http://localhost:8000/mypage/profile/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = "final.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "final.wsgi.application"
ASGI_APPLICATION = "final.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

AUTH_USER_MODEL = 'trip.User'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "trip",
        "USER": "blog_project_user",
        "PASSWORD": "1234",
        "HOST": "blog-project-db.cgoq8zivseqk.ap-northeast-2.rds.amazonaws.com",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'trip.User'

#로그인 안될시 리다이렉트
LOGIN_URL = '/login/'

# 실시간 채팅 설정

ASGI_APPLICATION = "final.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# AWS Setting
AWS_REGION = 'ap-northeast-2' #AWS서버의 지역
AWS_STORAGE_BUCKET_NAME = json_data['AWS_BUCKET_NAME'] #생성한 버킷 이름
AWS_ACCESS_KEY_ID = json_data['AWS_ACCESS_KEY'] #액서스 키 ID
AWS_SECRET_ACCESS_KEY = json_data['AWS_SERCRET_ACCESS_KEY'] #액서스 키 PW
#버킷이름.s3.AWS서버지역.amazonaws.com 형식
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)

#미디어 파일  설정
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = BASE_DIR / "media"