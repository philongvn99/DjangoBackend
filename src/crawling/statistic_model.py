from typing import List

class Competition:
    abbreviation: str
    description: str
    level: str
    source: str
    id: int

class CompSeason:
    label: str
    id: int
    
class Ground:
    name: str
    city: str
    source: str
    id: int
    
class Clock:
    secs: int
    label:str 

class Club:
    name: str
    shortName: str
    abbr: str
    id: int
    
class TeamInfo:
    name: str
    club: Club
    teamType: str
    shortName:str
    id: int

class Team:
    team: TeamInfo
    score: int

class GameWeek:
    id: int
    gameweek: int
    compSeason: CompSeason

class KickOff:
    completeness: int
    millis: int
    label: str
    
class MatchInfo:
    gameweek: GameWeek
    kickoff: KickOff
    provisionalKickoff: KickOff
    teams: List[Team]
    replay: bool
    ground: Ground
    neutralGround: bool
    status: str
    phase: str
    outcome: str
    attendance: 62462
    clock: Clock
    fixtureType: str
    extraTime: bool
    shootout: bool
    behindClosedDoors: bool
    id: int

class Statistic:
    name: int
    
class TeamStat:
    M: List[Statistic]


class MatchStaistic:
     entity: MatchInfo
     data: dict[str, TeamStat]   