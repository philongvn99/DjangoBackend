import json
import psycopg2
from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator

# Create your models here.    
# ==============================================================//
class Player(models.Model):
    ROLES = [
        ("GOALKEEPER", "GOALKEEPERS"),
        ("DEFENDER", "DEFENDER"),
        ("MIDFIELDER", "MIDFIELDER"),
        ("FORWARD", "FORWARD"),
    ]
    STATUSES = [
        ("ACTIVE", "ACTIVE"),
        ("LOAN", "LOAN"),
        ("LEFT", "LEFT"),
    ]
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=256)
    player_full_name = models.CharField(max_length=256)
    player_avatar_link = models.CharField(max_length=256)
    player_nationality = models.CharField(max_length=30)
    player_birthday = models.DateField()
    player_right_foot = models.BooleanField()
    player_kit_number = models.IntegerField()
    player_height = models.IntegerField()
    player_role = models.TextField(choices=ROLES, null=True) 
    player_salary = models.IntegerField(blank=True, null=True)
    player_status = models.TextField(choices=STATUSES, null=True)

    class Meta:
        managed = False
        db_table = 'tb_player'
        ordering = ['player_birthday']
        
    def __str__(self):
        return self.player_name

    
