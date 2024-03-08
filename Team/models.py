from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from django.db import models
from fake_useragent import UserAgent

from common import postgresql as pg
from common import support as sp

# Create your models here.    


ua = UserAgent()
class Team(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    name = models.CharField(max_length=50, blank=True, null=True, db_column="str_name")
    acronym_name = models.CharField(max_length=50, blank=True, null=True, db_column="str_acronym_name")
    logo_link = models.CharField(max_length=100, blank=True, null=True, db_column="str_logo_link")
    location = models.CharField(max_length=32, blank=True, null=True, db_column="str_location")


    class Meta:
        managed = False
        db_table = 'team'
        
    def __str__(self):
        return self.name
    
class League(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    name = models.CharField(max_length=50, blank=True, null=True, db_column="str_name")
    host = models.CharField(max_length=50, blank=True, null=True, db_column="n4_host")
    type = models.CharField(max_length=50, blank=True, null=True, db_column="n4_type")


    class Meta:
        managed = False
        db_table = 'league'
        
    def __str__(self):
        return self.name
    
class TeamAttendance(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    play = models.SmallIntegerField(db_column="n4_play")
    win = models.SmallIntegerField(db_column="n4_win")
    draw = models.SmallIntegerField(db_column="n4_draw")
    lost = models.SmallIntegerField(db_column="n4_lost")
    score = models.SmallIntegerField(db_column="n4_score")
    conceded = models.SmallIntegerField(db_column="n4_conceded")
    banned = models.SmallIntegerField(db_column="n4_banned")
    season = models.SmallIntegerField(db_column="n4_season")
    league = models.ForeignKey(League, models.DO_NOTHING, blank=True, null=True, db_column="n4_league_id")
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True, db_column="n4_team_id")
    
    class Meta:
        managed = False
        db_table = 'team_attendance'
        
    def __str__(self):
        return self.team.name + '-' + str(self.season)
    
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
        if teams[-1] == 'FT':
            results["home"].append(teams[1])
            results["away"].append(teams[4])
            results["score"][f'home{i}'] = int(score[1])
            results["score"][f'away{i}'] = int(score[3])
            i += 1
    return results