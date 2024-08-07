from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from django.contrib import admin
from django.db import models
from fake_useragent import UserAgent

from api.Team.models import League, TeamAttendance

# Create your models here.
ua = UserAgent()


# Create your models here.
# ==============================================================//
class Match(models.Model):
    id = models.AutoField(primary_key=True, db_column="n4_id")
    home = models.ForeignKey(
        TeamAttendance,
        models.CASCADE,
        null=False,
        db_column="n4_home_id",
        related_name="home_team",
    )
    away = models.ForeignKey(
        TeamAttendance,
        models.CASCADE,
        null=False,
        db_column="n4_away_id",
        related_name="away_team",
    )
    league = models.ForeignKey(
        League, models.CASCADE, null=False, db_column="n4_league_id"
    )
    round = models.IntegerField(blank=True, null=False, db_column="n4_round")
    fthg = models.IntegerField(blank=True, null=False, db_column="n4_fthg")
    ftag = models.IntegerField(blank=True, null=False, db_column="n4_ftag")
    str_date = models.CharField(max_length=50, blank=True, null=True)
    external_id = models.IntegerField(blank=True, null=True, db_column="n4_external_id")

    class Meta:
        managed = True
        db_table = "match"

    def __str__(self):
        return (
            self.home.__str__()
            + " vs "
            + self.away.__str__()
            + " "
            + self.league.__str__()
            + " "
            + self.round.__str__()
        )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("home", "away", "league_id", "round")


# ------------------------- LEAGUE FUNCTIONs ---------------------------------------------------
def get_league_results_by_date(date_string: str):
    match_req = Request(
        f"https://www.espn.com/soccer/fixtures/_/date/{date_string}/league/eng.1"
    )
    match_req.add_header("User-Agent", ua.random)
    print(f"https://www.espn.com/soccer/fixtures/_/date/{date_string}/league/eng.1")
    with urlopen(match_req) as req:
        match_doc = req.read().decode("utf8")
        soup = BeautifulSoup(match_doc, "html.parser")

        result_soup = soup.select("tbody>tr.Table__TR")
        results = {"home": [], "away": [], "home_score": [], "away_score": []}

        i = 0
        for res in result_soup[:20]:
            teams = [team.text for team in res.select("a.AnchorLink")]
            score = res.find("a", {"class": "AnchorLink at"}).text.split(" ")
            if teams[-1] == "FT":
                results["home"].append(teams[1])
                results["away"].append(teams[4])
                results["home_score"].append(score[1])
                results["away_score"].append(score[3])
                i += 1
        return results


def get_epl_results_by_round(match_week: int):
    match_week_req = Request(
        f"https://www.premierleague.com/matchweek/{match_week + 12268}/blog?match=true"
    )
    match_week_req.add_header("User-Agent", ua.random)
    with urlopen(match_week_req) as match_week_doc:
        doc = match_week_doc.read().decode("utf8")
        match_results = list(
            [
                m.attrs["href"].split("/")[-1],
                m.select_one("span.match-fixture__score").text.split("-"),
                [team.text for team in m.select("div>span.match-fixture__team-name")],
            ]
            for m in BeautifulSoup(doc, "html.parser").select(
                "a.match-fixture--abridged"
            )
        )
        return match_results
