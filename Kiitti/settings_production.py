from settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ('.kiitti.fi',)

STATIC_ROOT = '/var/www/staticfiles/kiitti-backend-admin'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'kiittidb',
#         'USER': 'kiitti',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '', # 5432
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),
    }
}
