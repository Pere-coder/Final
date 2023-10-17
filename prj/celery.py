import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

app = Celery('prj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.worker_concurrency = 1
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')