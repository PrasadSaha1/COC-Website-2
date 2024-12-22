from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class SavedClan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_clans')
    clan_tag = models.CharField(max_length=20)

    def __str__(self):
        return self.clan_tag
    
class SavedPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_players')
    player_tag = models.CharField(max_length=20)

    def __str__(self):
        return self.player_tag
    
class GlobalPlayer(models.Model):
    player_tag = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.player_tag

class PlayerMonthlyData(models.Model):
    player = models.ForeignKey(GlobalPlayer, on_delete=models.CASCADE, related_name='monthly_data')
    
    month = models.CharField(max_length=20, default="")  # Stores the month/year for the data
    year = models.IntegerField(default=0)

    town_hall_level = models.IntegerField()
    builder_hall_level = models.IntegerField()

    clan_name = models.CharField(max_length=20)
    clan_tag = models.CharField(max_length=20)

    trophies = models.IntegerField(default=0)
    builder_base_trophies = models.IntegerField(default=0)
    war_stars = models.IntegerField(default=0)
    XP_level = models.IntegerField(default=0)

    hero_data = models.JSONField(default=list)
    equipment_data = models.JSONField(default=list)
    troop_data = models.JSONField(default=list)
    spell_data = models.JSONField(default=list)

    # these are temporary 
    hour = models.IntegerField(default=7)  # To store the hour
    minute = models.IntegerField(default=7)  # To store the minute
    second = models.IntegerField(default=7)  # To store the second

    def __str__(self):
        return f"{self.player.player_tag}"