import datetime
from typing import List


class Ground:
    def __init__(self, input):
        self.name = input["name"]
        self.city = input["city"]


class TeamInfo:
    name: str
    shortName: str
    id: int

    def __init__(self, input):
        self.id = input["team"]["id"]
        self.name = input["team"]["name"]
        self.shortName = input["team"]["shortName"]


class MatchInfo:
    gameweekId: int
    matchId: int
    season: str
    round: int
    league: str
    kickoff: str
    groundName: Ground
    attendance: int

    def __init__(self, input):
        gameweek = input["gameweek"]
        self.gameweekId = gameweek["id"]
        self.matchId = input["id"]
        self.season = gameweek["compSeason"]["label"]
        self.round = gameweek["gameweek"]
        self.league = gameweek["compSeason"]["competition"]["description"]
        self.kickoff = datetime.datetime.strptime(
            input["kickoff"]["label"][:-4], "%a %d %b %Y, %H:%M"
        ).strftime("%d/%m/%Y")
        self.groundName = Ground(input["ground"])
        self.attendance = input.get("attendance", 0)


class Statistic(dict):
    ftg: int  # fulltime goal
    htg: int  # halftime goal
    sh: int  # shot
    sot: int  # shot on target
    co: int  # corner
    fo: int  # foul
    yc: int  # yellow carde
    rc: int  # red card

    def __init__(self):
        self.ftg = 0
        self.htg = 0
        self.sh = 0
        self.sot = 0
        self.co = 0
        self.fo = 0
        self.yc = 0
        self.rc = 0


class TeamStat:
    info: TeamInfo
    stats: Statistic

    def __init__(self, input: dict):
        self.info = TeamInfo(input)
        self.stats = Statistic()


class MatchStatistic:
    match: MatchInfo
    team1: TeamStat
    team2: TeamStat

    def __init__(self, input: dict):
        self.match = MatchInfo(input["entity"])

        self.team1 = TeamStat(input["entity"]["teams"][0])
        self.team2 = TeamStat(input["entity"]["teams"][1])

        self.team1.stats.ftg = input["entity"]["teams"][0]["score"]
        self.team2.stats.ftg = input["entity"]["teams"][1]["score"]

    def get_stats(self, input):
        for stat in input["data"][str(self.team1.info.id)]["M"]:
            if stat["name"] == "first_half_goals":
                self.team1.stats.htg = stat["value"]
            elif stat["name"] == "total_scoring_att":
                self.team1.stats.sh = stat["value"]
            elif stat["name"] == "ontarget_scoring_att":
                self.team1.stats.sot = stat["value"]
            elif stat["name"] == "total_corners_intobox":
                self.team1.stats.co = stat["value"]
            elif stat["name"] == "fk_foul_lost":
                self.team1.stats.fo = stat["value"]
            elif stat["name"] == "total_yel_card":
                self.team1.stats.yc = stat["value"]
            elif stat["name"] == "total_red_card":
                self.team1.stats.rc = stat["value"]

        for stat in input["data"][str(self.team2.info.id)]["M"]:
            if stat["name"] == "first_half_goals":
                self.team2.stats.htg = stat["value"]
            elif stat["name"] == "total_scoring_att":
                self.team2.stats.sh = stat["value"]
            elif stat["name"] == "ontarget_scoring_att":
                self.team2.stats.sot = stat["value"]
            elif stat["name"] == "total_corners_intobox":
                self.team2.stats.co = stat["value"]
            elif stat["name"] == "fk_foul_lost":
                self.team2.stats.fo = stat["value"]
            elif stat["name"] == "total_yel_card":
                self.team2.stats.yc = stat["value"]
            elif stat["name"] == "total_red_card":
                self.team2.stats.rc = stat["value"]
