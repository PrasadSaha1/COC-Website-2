from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'COC_app.settings')

app = Celery('COC_app')  
# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'run-scheduled-task-on-12-22-24': {
        'task': 'main.tasks.update_player_history',  # Update to the correct task path
        'schedule': crontab(minute=0, hour=1, day_of_month=22, month_of_year=12),  # Runs at 1 AM on 12/22/24
    },
}

# Optional: to use timezone-aware scheduling
app.conf.timezone = 'America/New_York'  # Set to the timezone you want (EST for Eastern Standard Time)
app.conf.update(
    worker_pool='solo'  # Disable multiprocessing
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

