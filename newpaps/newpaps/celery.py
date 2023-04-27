import os
from celery import Celery
from celery.schedules import crontab


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'action',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_old',
        'schedule': crontab(),
    },
}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpaps.settings')

app = Celery('newpaps')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
