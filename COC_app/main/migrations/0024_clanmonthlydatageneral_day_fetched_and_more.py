# Generated by Django 5.1.3 on 2024-12-23 21:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_clanmonthlydatageneral_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='clanmonthlydatageneral',
            name='day_fetched',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='clanmonthlydatageneral',
            name='month_year',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
