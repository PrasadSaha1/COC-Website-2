# Generated by Django 5.1.3 on 2024-12-24 23:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_remove_playermonthlydata_day_fetched_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermonthlydata',
            name='day_fetched',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
