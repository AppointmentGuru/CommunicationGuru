import os

def get_secret(secret_name, default=None):
    '''Returns a docker secret'''
    try:
        return open('/run/secrets/{}'.format(secret_name)).read().rstrip()
    except FileNotFoundError:
        return os.environ.get(secret_name, default)

ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", '').split(',')]

# aws storage
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'eu-central-1'
# AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
STATIC_URL = "https://s3.amazonaws.com/{}/".format(AWS_STORAGE_BUCKET_NAME)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# database:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': 5432,
    }
}
db_password = os.environ.get('DATABASE_PASSWORD', False)
if db_password:
    DATABASES.get('default').update({'PASSWORD': db_password})

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'kong_oauth.drf_authbackends.KongDownstreamAuthHeadersAuthentication',
    )
}

SANDBOX_MODE = os.environ.get('SANDBOX_MODE', 'True') == 'True'
SANDBOX_SMS = os.environ.get('SANDBOX_SMS')
# SMS / TWILLIO
TWILLIO_SID = os.environ.get('TWILLIO_SID')
TWILLIO_AUTH_TOKEN = os.environ.get('TWILLIO_AUTH_TOKEN')
TWILLIO_PHONE_NUMBER = os.environ.get('TWILLIO_PHONE_NUMBER')
TWILLIO_STATUS_CALLBACK = "https://communicationguru.appointmentguru.co/incoming/slack/"

ZOOM_BASE_URL = 'https://www.zoomconnect.com:443'
ZOOM_API_TOKEN = os.environ.get('ZOOM_AUTH_TOKEN')
ZOOM_EMAIL = 'tech@appointmentguru.co'

# EMAIL / MailGun

ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SENDER_DOMAIN'),
    'WEBHOOK_AUTHORIZATION': os.environ.get('WEBHOOK_AUTHORIZATION'),
}
MAILGUN_API_URL = 'https://api.mailgun.net'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_ALWAYS_EAGER = os.environ.get('CELERY_ALWAYS_EAGER', 'False') == 'True'

SMS_BACKEND = os.environ.get('SMS_BACKEND')
DEFAULT_IN_APP_BACKEND = os.environ.get('DEFAULT_IN_APP_BACKEND')

BACKENDS = [
    'services.backends.email.EmailBackend',
    'services.backends.onesignal.OneSignalBackend',
    'services.backends.zoomconnect.ZoomSMSBackend',
]

ALLOWED_TASK_MODULES = {
    'api.helpers'
}
TASKENGINE_API_KEY = 'D94AE07E-EEC1-4D7C-AC48-91E135779516'

DEFAULT_EMAIL_MESSAGE_BACKEND = 'services.backends.email.EmailBackend'
DEFAULT_SHORT_MESSAGE_BACKEND = os.environ.get('DEFAULT_SHORT_MESSAGE_BACKEND')
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"  # or sendgrid.SendGridBackend, or...

NOSQL_BACKENDS = os.environ.get('NOSQL_BACKENDS', '').split(',')
#  FireStore settings
FIRESTORE_CREDENTIALS_FILE = os.environ.get(
    'FIRESTORE_CREDENTIALS_FILE',
    '/code/firestore-credentials.json'
)

DEBUG = os.environ.get('DEBUG') == 'True'