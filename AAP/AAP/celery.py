from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AAP.settings')

app = Celery('AAP')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

from celery.schedules import crontab

app.conf.beat_schedule = {
    'parse_avito': {
        'task': 'parse_avito',
        'schedule': 360.0,
        'args': (),
    },
}