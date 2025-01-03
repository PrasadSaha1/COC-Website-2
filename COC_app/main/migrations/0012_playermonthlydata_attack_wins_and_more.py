# Generated by Django 5.1.3 on 2024-12-22 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_playermonthlydata_second_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermonthlydata',
            name='attack_wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='clan_capital_contributions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='defense_wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='donations_given',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playermonthlydata',
            name='donations_recieved',
            field=models.IntegerField(default=0),
        ),
    ]
