import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpaps.settings')

app = Celery('newpaps')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
