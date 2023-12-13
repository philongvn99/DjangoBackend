from django.db import models
from Team.models import GroupStageTeam
from Player.models import Player

# Create your models here.    
# ==============================================================//
class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_enemy = models.ForeignKey(GroupStageTeam, models.DO_NOTHING)
    match_stadium = models.CharField(max_length=256)
    match_home = models.BooleanField()
    match_home_score = models.IntegerField(blank=True, null=True)
    match_enemy_score = models.IntegerField(blank=True, null=True)
    match_date = models.DateField(blank=True, null=True)
    match_lineup = models.CharField(max_length=5, blank=True, null=True)
    match_referee = models.CharField(max_length=256, blank=True, null=True)
    match_type = models.TextField(blank=True, null=True) 
    class Meta:
        managed = False
        db_table = 'tb_match'
        

class GoalScore(models.Model):
    gs_player = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    gs_match = models.ForeignKey(Match, models.DO_NOTHING, blank=True, null=True)
    gs_minute = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'r_goalscore'


class OwnGoal(models.Model):
    og_player = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    og_match = models.ForeignKey(Match, models.DO_NOTHING, blank=True, null=True)
    og_minute = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'r_owngoal'


class RedCard(models.Model):
    rc_player = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    rc_match = models.ForeignKey(Match, models.DO_NOTHING, blank=True, null=True)
    rc_minute = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'r_redcard'


class YellowCard(models.Model):
    yc_player = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    yc_match = models.ForeignKey(Match, models.DO_NOTHING, blank=True, null=True)
    yc_minute = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'r_yellowcard'