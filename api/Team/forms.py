from django import forms

from api.Team import models


class NewTeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = "__all__"


class TeamAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.TeamAttendance
        fields = "__all__"
