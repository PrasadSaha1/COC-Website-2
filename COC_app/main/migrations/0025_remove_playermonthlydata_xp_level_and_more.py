# Generated by Django 5.1.3 on 2024-12-24 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_clanmonthlydatageneral_day_fetched_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='XP_level',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='attack_wins',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='builder_base_trophies',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='builder_hall_level',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='clan_capital_contributions',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='clan_name',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='clan_tag',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='day',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='defense_wins',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='donations_given',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='donations_recieved',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='equipment_data',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='hero_data',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='hour',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='minute',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='month',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='player_name',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='spell_data',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='town_hall_level',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='troop_data',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='trophies',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='war_stars',
        ),
        migrations.RemoveField(
            model_name='playermonthlydata',
            name='year',
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='data',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='day_fetched',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='month_year',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
