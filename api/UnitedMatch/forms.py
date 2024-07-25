from django import forms

from api.UnitedMatch import models


class NewUnitedMatchForm(forms.ModelForm):
    class Meta:
        model = models.UnitedMatch
        fields = "__all__"
