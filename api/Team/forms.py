from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from api.Team import models

from src.common import postgresql as pg
from src.common import support as sp


class NewTeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = "__all__"


class NewTeamAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.TeamAttendance
        fields = "__all__"


class LeagueResultForm(forms.BaseForm):
    id_list = SimpleArrayField(forms.IntegerField())
    goalscore_list = SimpleArrayField(forms.IntegerField())
    goalconceded_list = SimpleArrayField(forms.IntegerField())
    data_len = forms.IntegerField(max_value=20, min_value=10)

    def __init__(self, data):
        self.id_list = data["id"]
        self.goalscore_list = data["goalscore"]
        self.goalconceded_list = data["goalconceded"]
        self.data_len = len(data["id"])
        forms.BaseForm.__init__(self)


def update_league_table(data: LeagueResultForm):
    res = []
    pg.cursorDB.execute(
        f"""SELECT * from update_league_table(
            ARRAY {data.id_list},
            ARRAY {data.goalscore_list},
            ARRAY {data.goalconceded_list},
            {data.data_len},
            'PREMIER_LEAGUE',
            2023)"""
    )
    pg.connectionPG.commit()
    return_record = pg.cursorDB.fetchall()
    if return_record == []:
        return None
    for record in return_record:
        res.append(dict(zip(sp.teamAttendanceFields, record)))
    return res
