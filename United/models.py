import json
import psycopg2
from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator

from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from . import support as sp

# Create your models here.    

# ===========================INITIAL PSYCOPG2===================//
connectionPG = psycopg2.connect(
    user="philong249",
    password="01886933234",
    host="localhost",
    port="5432",
    database="plpostgres_database",
)
cursorDB = connectionPG.cursor()
cursorDB.execute("SELECT version();")
record = cursorDB.fetchone()
ua = UserAgent()
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

    
class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=256)
    account_email = models.CharField(max_length=256)
    account_username = models.CharField(max_length=256)
    account_phone = models.CharField(max_length=256)
    account_name = models.CharField(max_length=256)
    account_password = models.CharField(max_length=256)
    account_role = models.TextField()  # This field type is a guess.
    account_license_plate = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account'
        
class Team(models.Model):
    team_id = models.CharField(primary_key=True, max_length=10)
    team_name = models.CharField(max_length=256, blank=True, null=True)
    team_acronym_name = models.CharField(max_length=256, blank=True, null=True)
    team_logo_link = models.CharField(max_length=256, blank=True, null=True)
    team_association = models.CharField(max_length=10, blank=True, null=True)
    team_location = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_team'
        
    def __str__(self):
        return self.team_name
class GroupStageTeam(models.Model):
    group_stage_team_id = models.CharField(primary_key=True, max_length=10)
    team_played_game = models.IntegerField()
    team_won_game = models.IntegerField()
    team_drawn_game = models.IntegerField()
    team_lost_game = models.IntegerField()
    team_goal_for = models.IntegerField()
    team_goal_against = models.IntegerField()
    team_goal_difference = models.IntegerField()
    team_points = models.IntegerField()
    team_league = models.TextField()  # This field type is a guess.
    team_season = models.SmallIntegerField()
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tb_group_stage_team'
        
    def __str__(self):
        return self.team_name

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
    match_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    
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

# LEAGUE----------------------------------------------------------------------------
def updateLeagueTable(idList, gsList, gcList, nTeam):
    res = []
    cursorDB.execute(
        """SELECT * from update_league_table( ARRAY %s, ARRAY %s, ARRAY %s, %s, 'PREMIER_LEAGUE', 2023)"""
        % (idList, gsList, gcList, nTeam)
    )
    connectionPG.commit()
    returnRecord = cursorDB.fetchall()
    if returnRecord == []:
        return None
    for record in returnRecord:
        res.append(dict(zip(sp.leagueTableField, record)))
    return res

def getLeagueResults(dateString:str):       
    match_req = Request(f'https://www.espn.com/soccer/fixtures/_/date/{dateString}/league/eng.1')
    match_req.add_header('User-Agent', ua.random)
    match_doc = urlopen(match_req).read().decode('utf8')
    
    soup = BeautifulSoup(match_doc, 'html.parser')
        
    resultSoup = soup.select("tbody>tr.Table__TR")
    results = {"home": [], "away": [], "score": {}}

    i = 0
    for res in resultSoup[:10]:
        teams = [team.text for team in res.select("a.AnchorLink")]
        score = res.find("a", {"class": "AnchorLink at"}).text.split(' ')
        if len(score) > 1:
            results["home"].append(teams[1])
            results["away"].append(teams[4])
            results["score"][f'home{i}'] = int(score[1])
            results["score"][f'away{i}'] = int(score[3])
            i += 1
    return results