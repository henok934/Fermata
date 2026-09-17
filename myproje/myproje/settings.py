import os
from pathlib import Path
from dotenv import load_dotenv
TURNSTILE_SITE_KEY = os.getenv("TURNSTILE_SITE_KEY", "1x00000000000000000000AA")
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY", "1x0000000000000000000000000000000AA")

#TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY", "1x0000000000000000000000000000000AA")
# 1. BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file explicitly from Project Root
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 2. SECURITY CONFIGURATIONS
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fbchw3&+vaut7yj4c9$jz$a=9r40d-zp&=be32@5hu_+wi1=zh')

#DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

DJANGO_DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# ወይም በቀጥታ
DEBUG = False # ፕንትስት (penetration test) ወይም ሰርተፍኬት ልታስገባ ስትል በቀጥታ False ማድረግ ይመረጣል

#TELEBIRR_NOTIFY_URL = "https://value-shortly-unveiled.ngrok-free.dev/api/telebirr/callback/"
ALLOWED_HOSTS = [
    'value-shortly-unveiled.ngrok-free.dev',
    '196.191.95.76',
    'busfermata.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Security Options
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Reverse Proxy (Nginx) ስላለ False መሆኑ ትክክል ነው
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party Apps
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'axes',
    'turnstile', 

    # Project Apps
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'myproje.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # <-- '.django' እዚህ ጋር ተጨምሯል
        'DIRS': [os.path.join(BASE_DIR, 'users/templates')],
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


WSGI_APPLICATION = 'myproje.wsgi.application'

# 4. DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 5. AUTHENTICATION & USERS
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_ENABLED = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'hibir-auth-ratelimit-protector',
    }
}

TURNSTILE_SITE_KEY = os.environ.get('TURNSTILE_SITE_KEY', '0x4AAAAAAAM1_xxxxxxxxxxxx')
TURNSTILE_SECRET_KEY = os.environ.get('TURNSTILE_SECRET_KEY', '0x4AAAAAAAM1_xxxxxxxxxxxx')

# 6. EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'teklemariammossie1@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'teklemariammossie697@gmail.com')

# 7. STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'users/static')]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 8. CORS & CSRF CONFIGURATIONS
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'https://value-shortly-unveiled.ngrok-free.dev',
    'https://196.191.95.76',
    'https://busfermata.onrender.com',
]

# 9. INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Addis_Ababa'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 10. REST FRAMEWORK & SPECTACULAR
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Busfermata Digital Technology API',
    'DESCRIPTION': 'Cross-Country Bus Fleet Management & Electronic Ticketing API Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# 11. TELEBIRR PAYMENT INTEGRATION SETTINGS

raw_private_key = os.environ.get("TELEBIRR_PRIVATE_KEY", "")
raw_public_key = os.environ.get("TELEBIRR_PUBLIC_KEY", "")
notify_url_env = os.environ.get("TELEBIRR_NOTIFY_URL", "").strip()
redirect_url_env = os.environ.get("TELEBIRR_REDIRECT_URL", "").strip()

TELEBIRR_CONFIG = {
     "BASE_URL": os.environ.get(
        "TELEBIRR_BASE_URL", "https://developerportal.ethiotelecom.et:38443"
    ),
    "WEB_BASE_URL": os.environ.get(
        "TELEBIRR_WEB_BASE_URL",
        "https://developerportal.ethiotelecom.et:38443/pay/",
    ),

    "merchantCode": os.environ.get("TELEBIRR_MERCHANT_CODE", "259159"),
    "merchantAppId": os.environ.get(
        "TELEBIRR_MERCHANT_APP_ID", "1674185087411200"
    ),
    "fabricAppId": os.environ.get(
        "TELEBIRR_FABRIC_APP_ID", "c4182ef8-9249-458a-985e-06d191f4d505"
    ),
    "appSecret": os.environ.get(
        "TELEBIRR_APP_SECRET", "fad0f06383c6297f545876694b974599"
    ),

    "notify_url": os.environ.get("TELEBIRR_NOTIFY_URL", "https://value-shortly-unveiled.ngrok-free.dev/api/telebirr/callback/"),
    "redirect_url": os.environ.get("TELEBIRR_REDIRECT_URL", "https://value-shortly-unveiled.ngrok-free.dev/users/telebirr-redirect/"),
    "PRIVATE_KEY": raw_private_key.replace("\\n", "\n") if raw_private_key else "",
    "PUBLIC_KEY": raw_public_key.replace("\\n", "\n") if raw_public_key else "",
}

# Session Cache Configurations
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
