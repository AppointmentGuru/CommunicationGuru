from .tasks import ping
from django_celery_results.models import TaskResult
from django.utils import timezone
from datetime import timedelta
import requests, os

def db_connected(modelclass):
    return modelclass.objects.first()

def celery_working():
    task = ping.apply()
    assert task.status == 'SUCCESS',\
        'Error when queuing a task'

def rabbit_is_up(
    rabbit_user=os.environ.get('RABBITMQ_DEFAULT_USER'),
    rabbit_password=os.environ.get('RABBITMQ_DEFAULT_PASS')):
    url = 'http://{}:15672/api/healthchecks/node'.format(os.environ.get('RABBITMQ_DEFAULT_HOST'))
    rabbit_status = requests.get(url, auth=(rabbit_user, rabbit_password))
    assert rabbit_status.json().get('status') == 'ok',\
        'Issues connecting to rabbit: {}'.format(rabbit_status.content)
    return rabbit_status

def failed_tasks_count(minutes_back=5, failure_threshold=0):
    time_window = (timezone.now() - timedelta(minutes=minutes_back))
    failed_tasks = TaskResult.objects.exclude(status='SUCCESS').filter(date_done__gte=time_window)

    assert failed_tasks.count() <= failure_threshold,\
        'There are too many failed tasks: {}'.format(failed_tasks.count())
    return failed_tasks
