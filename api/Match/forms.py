from django import forms


class MatchResultForm(forms.Form):
    goalscore = forms.IntegerField(required=True)
    goalconceded = forms.IntegerField(required=True)
    hometeam = forms.CharField(min_length=8, max_length=20)
    awayteam = forms.CharField(min_length=8, max_length=20)
    home_goalscorer = forms.CharField(min_length=8, max_length=20)
    away_goalscorer = forms.CharField(min_length=8, max_length=20)
    home_yellowcard = forms.CharField(min_length=8, max_length=20)
    home_redcard = forms.CharField(min_length=8, max_length=20)
    league = forms.CharField(min_length=8, max_length=20)
