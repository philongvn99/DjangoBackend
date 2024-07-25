from django.contrib import admin
from django.db import models

from api.Player.models import Player
from api.Team.models import TeamAttendance


# Create your models here.
# ==============================================================//
class UnitedMatch(models.Model):
    match_id = models.AutoField(primary_key=True, db_column="n4_id")
    match_enemy = models.ForeignKey(
        TeamAttendance, models.CASCADE, null=False, db_column="n4_enemy_id"
    )
    match_stadium = models.CharField(max_length=50, db_column="str_name")
    match_home = models.BooleanField()
    match_home_score = models.IntegerField(blank=True, null=True)
    match_enemy_score = models.IntegerField(blank=True, null=True)
    match_date = models.DateField(blank=True, null=True)
    match_lineup = models.CharField(max_length=5, blank=True, null=True)
    match_referee = models.CharField(max_length=50, blank=True, null=True)
    match_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "united_match"

    def __str__(self):
        return self.match_enemy.__str__() + " " + self.match_type


@admin.register(UnitedMatch)
class UnitedMatchAdmin(admin.ModelAdmin):
    list_display = ("match_enemy", "match_date", "match_type")


class UnitedMatchEvent(models.Model):
    MATCH_PARTS = [
        ("FIRST_LEG", "FIRST_LEG"),
        ("SECOND_LEG", "SECOND_LEG"),
        ("SUB_FIRST", "SUB_FIRST"),
        ("SUB_SECOND", "SUB_SECOND"),
        ("PENALTY", "PENALTY"),
        ("SUBSTITUTE_IN", "SUBSTITUTE_IN"),
    ]
    MATCH_TYPE = [
        ("RED_CARD", "RED_CARD"),
        ("YELLOW_CARD", "YELLOW_CARD"),
        ("GOAL", "GOAL"),
        ("OWN_GOAL", "OWN_GOAL"),
        ("SUBSTITUTE_OUT", "SUBSTITUTE_OUT"),
        ("OUT_OF_TIME", "OUT_OF_TIME"),
    ]
    id = models.AutoField(primary_key=True, db_column="n4_id")
    match = models.ForeignKey(
        UnitedMatch, models.CASCADE, blank=True, null=False, db_column="n4_match_id"
    )
    player = models.ForeignKey(
        Player, models.CASCADE, blank=True, null=False, db_column="n4_player_id"
    )
    minute = models.IntegerField(db_column="n4_minute")
    part = models.TextField(choices=MATCH_PARTS, null=True, db_column="str_half")
    type = models.TextField(choices=MATCH_TYPE, null=True, db_column="str_type")

    class Meta:
        managed = True
        db_table = "united_match_event"


@admin.register(UnitedMatchEvent)
class UnitedMatchEventAdmin(admin.ModelAdmin):
    list_display = ("match", "player", "minute", "type")
