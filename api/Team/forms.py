from django import forms

from api.Team import models


class NewTeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = "__all__"


class NewTeamAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.TeamAttendance
        fields = "__all__"


class LeagueMatchResultForm(forms.Form):
    home_id = forms.IntegerField(min_value=0)
    away_id = forms.IntegerField(min_value=0)
    home = forms.IntegerField(min_value=0)
    away = forms.IntegerField(min_value=0)


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


def convert_result_2_point(result_form: list[LeagueMatchResultForm]):
    res: dict[int, TeamUpdateData] = {}
    for form in result_form:
        cleaned = form.cleaned_data
        home_id = cleaned["home_id"]
        away_id = cleaned["away_id"]
        home = cleaned["home"]
        away = cleaned["away"]

        if home_id in res:
            res[home_id].update(home, away)
        else:
            res[home_id] = TeamUpdateData(home, away)

        if away_id in res:
            res[away_id].update(away, home)
        else:
            res[away_id] = TeamUpdateData(away, home)

    return res
