from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'COC_app.settings')

app = Celery('COC_app')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'fetch-clan-war-status': {
        'task': 'main.tasks.get_clan_war_status',  # Update to the correct task path
        'schedule': timedelta(hours=46),  # Runs every 46 hours
    },
}

app.conf.beat_schedule = {
    'update-monthly-clan-war-information': {
        'task': 'main.tasks.update_player_history',  # Update to your correct task path
        'schedule': crontab(minute=15, hour=13, day_of_month=23),  # Runs at midnight (00:00) on the 3rd of each month
    },
}


# Optional: to use timezone-aware scheduling
app.conf.timezone = 'America/New_York'  # Set to the timezone you want (EST for Eastern Standard Time)

# Optional Celery configuration for worker pool
app.conf.update(
    worker_pool='solo'  # Disable multiprocessing
)

# Autodiscover tasks from the Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
