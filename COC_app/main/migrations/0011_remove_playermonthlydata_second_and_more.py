# Generated by Django 5.1.3 on 2024-12-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_playermonthlydata_builder_base_trophies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='second',
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='day',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playermonthlydata',
            name='month',
            field=models.IntegerField(default=0),
        ),
    ]
