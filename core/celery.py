import os
from celery import Celery

#create enviroment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#define celery app
app = Celery('core')

app.conf.update(
    worker_pool='solo',
)

#point to settings
app.config_from_object('django.conf.settings', namespace='CELERY')

#get all tasks to celery
app.autodiscover_tasks()

#log current task
@app.task(bind=True)
def debug(self):
    print(f'Request: {self.request!r}')