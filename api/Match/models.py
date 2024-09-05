import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from django.contrib import admin
from django.db import models
from fake_useragent import UserAgent

from api.Match.forms import BsObject
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


def get_epl_results_by_round(season: int, match_week: int):
    season_start_id = {2025: 18389, 2024: 12268, 2023: 7830}
    match_week_req = Request(
        f"https://www.premierleague.com/matchweek/{match_week + season_start_id[season]}/"
        f"blog?match=true"
    )
    match_week_req.add_header("User-Agent", ua.random)
    with urlopen(match_week_req) as match_week_doc:
        doc = match_week_doc.read().decode("utf8")
        match_results = list(
            [
                m.attrs["href"].split("/")[-1],
                (
                    m.select_one("span.match-fixture__score") or BsObject("100-100")
                ).text.split("-"),
                [team.text for team in m.select("div>span.match-fixture__team-name")],
            ]
            for m in BeautifulSoup(doc, "html.parser").select(
                "a.match-fixture--abridged"
            )
        )
        return match_results


def get_external_match_detail(match_id: str):
    match_stat_req = Request(
        f"https://footballapi.pulselive.com/football/stats/match/{match_id}"
    )
    match_stat_req.add_header("User-Agent", ua.random)
    match_stat_req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    )
    match_stat_req.add_header("Origin", "https://www.premierleague.com")
    match_stat_req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    match_stat_req.add_header(
        "Referer",
        "https://www.premierleague.com//clubs/1/Arsenal/squad?se=79",
    )
    with urlopen(match_stat_req) as query:
        decoded = query.read().decode("utf8")
        data = json.loads(decoded)
        return data


def update_remote_dynamodb(season: int, match_week: int):
    request = Request(
        f"https://mu5slwbyja.execute-api.ap-southeast-1.amazonaws.com/"
        f"default/league-season?"
        f"league=epl"
        f"&season={season}"
        f"&round={match_week}"
    )
    request.add_header("User-Agent", ua.random)
    request.get_method = lambda: "PATCH"
    with urlopen(request):
        return True
