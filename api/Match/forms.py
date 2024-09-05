from typing import Dict, List
from django import forms


class LeagueMatchForm(forms.Form):
    goalscore = forms.IntegerField(required=True)
    goalconceded = forms.IntegerField(required=True)
    hometeam = forms.CharField(min_length=8, max_length=20)
    awayteam = forms.CharField(min_length=8, max_length=20)
    home_goalscorer = forms.CharField(min_length=8, max_length=20)
    away_goalscorer = forms.CharField(min_length=8, max_length=20)
    home_yellowcard = forms.CharField(min_length=8, max_length=20)
    home_redcard = forms.CharField(min_length=8, max_length=20)
    league = forms.CharField(min_length=8, max_length=20)


class LeagueMatchResultForm(forms.Form):
    home_id = forms.IntegerField(min_value=0)
    away_id = forms.IntegerField(min_value=0)
    fthg = forms.IntegerField(min_value=0)
    ftag = forms.IntegerField(min_value=0)


class TeamUpdateData:
    def __init__(self, score: int, conceded: int):
        self.play = 1
        self.win = int(score > conceded)
        self.lost = int(score < conceded)
        self.draw = int(score == conceded)
        self.score = score
        self.conceded = conceded

    def update(self, score: int, conceded: int):
        self.play += 1
        if score > conceded:
            self.win += 1
        elif score == conceded:
            self.draw += 1
        else:
            self.lost += 1
        self.score += score
        self.conceded += conceded


def convert_result_2_point(result_form: List[LeagueMatchResultForm]):
    res: Dict[int, TeamUpdateData] = {}
    for form in result_form:
        cleaned = form.cleaned_data
        home_id = cleaned["home_id"]
        away_id = cleaned["away_id"]
        fthg = cleaned["fthg"]
        ftag = cleaned["ftag"]

        if home_id in res:
            res[home_id].update(fthg, ftag)
        else:
            res[home_id] = TeamUpdateData(fthg, ftag)

        if away_id in res:
            res[away_id].update(ftag, fthg)
        else:
            res[away_id] = TeamUpdateData(ftag, fthg)

    return res


class BsObject:
    def __init__(self, text):
        self.text = text
