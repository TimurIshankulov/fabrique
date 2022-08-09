import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabrique.settings')

app = Celery('fabrique')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'handle-mailings': {  # Beat task for handling mailings, see api.tasks.py
        'task': 'api.tasks.beat_handle_mailings',
        'schedule': crontab(minute='*/1')
    },
}
