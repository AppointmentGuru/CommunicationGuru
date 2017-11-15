from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communications.settings')

from django.conf import settings  # noqa
BROKER_URL = 'amqp://{}:{}@{}:5672//'.format(
    os.environ.get('RABBITMQ_DEFAULT_HOST'),
    os.environ.get('RABBITMQ_DEFAULT_USER'),
    os.environ.get('RABBITMQ_DEFAULT_PASS')
)
app = Celery('communications', broker=BROKER_URL, result_backend = 'rpc://')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
