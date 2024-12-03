from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.utils.timezone import now

# Установите переменную окружения для конфигурации Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endterm.settings')

# Создайте экземпляр Celery
app = Celery('endterm')

# Используйте настройки Django в Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()

app.conf.worker_pool = 'eventlet'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(rate_limit='1/m')
def check_preorders():
    from my_app.models import PreOrder
    """Check all pending preorders and mark them as completed if arrival_date is today."""
    today = now().date()
    print("check_preorders")
    preorders = PreOrder.objects.filter(arrival_date=today, status='pending')
    print(len(preorders), 'preorders')
    for preorder in preorders:
        preorder.complete_order()
    return f"{len(preorders)} preorders completed."


app.conf.beat_schedule = {
    'check-preorders-every-day': {
        'task': 'my_app.tasks.check_preorders',
        'schedule': crontab("*/1 * * * *"),
    },
}
