from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagement.settings')
app = Celery('StudentManagement')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.worker_pool = 'solo'
app.conf.broker_connection_retry_on_startup = True


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
