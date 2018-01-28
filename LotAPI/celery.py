import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LotAPI.settings')

app = Celery('LotAPI')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'task_name': {
        'task': 'lotAPP.tasks.close_lot',
        'schedule': crontab(minute='*/1')
    }
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))