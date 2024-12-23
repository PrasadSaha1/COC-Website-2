from django.db import models
from django.contrib.auth.models import User
from datetime import date

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

class PlayerWarInformation(models.Model):
    player = models.ForeignKey(GlobalPlayer, on_delete=models.CASCADE, related_name='war_information')

    date_started = models.DateField()
    clan_name = models.CharField(max_length=50)
    clan_tag = models.CharField(max_length=20)
    roster_number = models.IntegerField()
    num_attacks = models.IntegerField()
    num_missed_attacks = models.IntegerField(default=0)
    attack_1_stars = models.IntegerField()
    attack_1_destruction = models.IntegerField()
    attack_2_stars = models.IntegerField()
    attack_2_destruction = models.IntegerField()

class PlayerMonthlyData(models.Model):
    player = models.ForeignKey(GlobalPlayer, on_delete=models.CASCADE, related_name='monthly_data')
    
    day = models.IntegerField(default=0)
    month = models.IntegerField(default=0)  
    year = models.IntegerField(default=0)
    
    hour = models.IntegerField(default=7) 
    minute = models.IntegerField(default=7)  

    town_hall_level = models.IntegerField()
    builder_hall_level = models.IntegerField()
    player_name = models.CharField(max_length=50, default="N/A")

    clan_name = models.CharField(max_length=20)
    clan_tag = models.CharField(max_length=20)
    donations_given = models.IntegerField(default=0)
    donations_recieved = models.IntegerField(default=0)
    clan_capital_contributions = models.IntegerField(default=0)

    attack_wins = models.IntegerField(default=0)
    defense_wins = models.IntegerField(default=0)

    trophies = models.IntegerField(default=0)
    builder_base_trophies = models.IntegerField(default=0)
    war_stars = models.IntegerField(default=0)
    XP_level = models.IntegerField(default=0)

    hero_data = models.JSONField(default=list)
    equipment_data = models.JSONField(default=list)
    troop_data = models.JSONField(default=list)
    spell_data = models.JSONField(default=list)

    def __str__(self):
        return f"{self.player.player_tag}"

class PlayerMonthlyDataWar(models.Model):
    """Assumes a player does not change clan"""
    player = models.ForeignKey(GlobalPlayer, on_delete=models.CASCADE, related_name='monthly_data_war')

    num_wars = models.IntegerField()
    num_attacks = models.IntegerField()
    num_missed_attacks = models.IntegerField()
    total_stars = models.IntegerField()
    total_destruction = models.IntegerField()
    average_total_stars = models.FloatField()
    average_total_destruction = models.FloatField(default=0)

    clan_name = models.CharField(default="", max_length=50)
    clan_tag = models.CharField(max_length=20, default="")
    month_year = models.DateField(default=date.today)
    current_time = models.CharField(max_length=50, default="N/A")

class GlobalClan(models.Model):
    clan_tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.clan_tag

class ClanWarInformation(models.Model):
    clan = models.ForeignKey(GlobalClan, on_delete=models.CASCADE, related_name='war_information')
    war_info = models.JSONField(default=list)

class ClanMonthlyDataGeneral(models.Model):
    clan = models.ForeignKey(GlobalClan, on_delete=models.CASCADE, related_name='monthly_data_general')

class ClanMonthlyDataWar(models.Model):
    clan = models.ForeignKey(GlobalClan, on_delete=models.CASCADE, related_name='monthly_data_war')

    num_wars = models.FloatField(default=0.0)
    total_players = models.FloatField(default=0.0)
    total_stars = models.FloatField(default=0.0)
    total_destruction = models.FloatField(default=0.0)

    average_war_size = models.FloatField(default=0.0)
    average_total_stars = models.FloatField(default=0.0)
    average_stars_per_player = models.FloatField(default=0.0)
    average_total_destruction = models.FloatField(default=0.0)

    win_rate = models.FloatField(default=0.0)
    percent_attacks_completed = models.FloatField(default=0.0)

    month_year = models.DateField(default=date.today)
    current_time = models.CharField(max_length=50, default="N/A")
