from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator

from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from common import support as sp
from common import postgresql as pg

# Create your models here.    


ua = UserAgent()
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
        return self.team.team_name + '-' + str(self.team_season)
    
# ------------------------- LEAGUE FUNCTIONs ---------------------------------------------------
def updateLeagueTable(idList, gsList, gcList, nTeam):
    res = []
    pg.cursorDB.execute(
        """SELECT * from update_league_table( ARRAY %s, ARRAY %s, ARRAY %s, %s, 'PREMIER_LEAGUE', 2023)"""
        % (idList, gsList, gcList, nTeam)
    )
    pg.connectionPG.commit()
    returnRecord = pg.cursorDB.fetchall()
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