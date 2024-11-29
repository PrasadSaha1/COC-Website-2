from django.db import models
from django.contrib.auth.models import User

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
