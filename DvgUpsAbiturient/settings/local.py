from .base import *


DEBUG = True
load_dotenv(BASE_DIR / ".env.local")
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
INSTALLED_APPS += [
    'debug_toolbar',
]
MEDIA_ROOT = BASE_DIR / 'media'
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('POSTGRES_DB'),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": os.getenv('POSTGRES_HOST'),
        "PORT": os.getenv('POSTGRES_PORT'),
    }
}
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

ALLOWED_HOSTS = ["*"]

AUTH_PASSWORD_VALIDATORS = []
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CSRF_TRUSTED_ORIGINS = ['https://3355-185-48-112-240.ngrok-free.app', ]