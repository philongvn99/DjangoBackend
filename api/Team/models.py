from django.contrib import admin
from django.db import models


class Team(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    name = models.CharField(max_length=50, blank=True, null=True, db_column="str_name")
    acronym_name = models.CharField(
        max_length=50, blank=True, null=True, db_column="str_acronym_name"
    )
    logo_link = models.CharField(
        max_length=100, blank=True, null=True, db_column="str_logo_link"
    )
    location = models.CharField(
        max_length=32, blank=True, null=True, db_column="str_location"
    )

    class Meta:
        managed = True
        db_table = "team"

    def __str__(self):
        return self.name


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "location")


class League(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    name = models.CharField(max_length=50, blank=True, null=True, db_column="str_name")
    host = models.CharField(max_length=50, blank=True, null=True, db_column="str_host")
    type = models.CharField(max_length=50, blank=True, null=True, db_column="str_type")
    acronym_name = models.CharField(
        max_length=50, blank=True, null=True, db_column="str_acronym_name"
    )
    logo_link = models.CharField(
        max_length=200, blank=True, null=True, db_column="str_logo_link"
    )

    class Meta:
        managed = True
        db_table = "league"

    def __str__(self):
        return self.name


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name",)


class TeamAttendance(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    play = models.SmallIntegerField(db_column="n4_play", null=False, default=0)
    win = models.SmallIntegerField(db_column="n4_win", null=False, default=0)
    draw = models.SmallIntegerField(db_column="n4_draw", null=False, default=0)
    lost = models.SmallIntegerField(db_column="n4_lost", null=False, default=0)
    score = models.SmallIntegerField(db_column="n4_score", null=False, default=0)
    conceded = models.SmallIntegerField(db_column="n4_conceded", null=False, default=0)
    banned = models.SmallIntegerField(db_column="n4_banned", null=False, default=0)
    season = models.SmallIntegerField(db_column="n4_season", null=False, default=0)
    league = models.ForeignKey(
        League, models.DO_NOTHING, blank=True, null=True, db_column="n4_league_id"
    )
    team = models.ForeignKey(
        Team, models.DO_NOTHING, blank=True, null=True, db_column="n4_team_id"
    )

    class Meta:
        managed = True
        db_table = "team_attendance"

    def __str__(self):
        return self.team.name + "-" + str(self.season)


@admin.register(TeamAttendance)
class TeamAttendanceAdmin(admin.ModelAdmin):
    list_display = ("team", "league", "season")
    list_per_page = 20
    ordering = ("-season", "league")
