from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.validators import RegexValidator
from django.core.exceptions import NON_FIELD_ERRORS
from . import models, support as sp


loginValidator = [
    RegexValidator(
        r"^[a-zA-Z0-9]{7,32}$",
        message="Input must be Alphanumeric with maximum length 31",
    ),
]

phoneValidator = [
    RegexValidator(
        r"^\+84\d{9}$",
        message=("Phone number format: 9 digits following +84 (VIE)"),
    )
]

nameValidator = [
    RegexValidator(
        r"^[a-zA-Z]{2,}( [a-zA-Z]+)*$",
        message=("Phone number format: 9 digits following +84 (VIE)"),
    )
]


class LoginInfoForm(forms.Form):
    username = forms.CharField(min_length=8, max_length=32, validators=loginValidator)
    password = forms.CharField(min_length=7, max_length=32, validators=loginValidator)


class PlayerForm(forms.ModelForm):
    class Meta:
        model = models.Player
        fields = '__all__'
        error_messages = {
                NON_FIELD_ERRORS: {
                    'unique_together': "%(model_name)s's %(field_labels)s are not unique"}
            }
    def __str__(self):
        return self.cleaned_data.get('player_name')
    
class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = '__all__'
    def __str__(self):
        return self.cleaned_data.get('team_name')



class UserInfoForm(forms.Form):
    ROLES = [
        ("A", "Admin"),
        ("S", "Supporter"),
        ("U", "User"),
        ("G", "Guest"),
    ]

    def is_privileged(self):
        return self.role in {"A", "S"}

    def is_visible(self):
        return self.role in {"A", "S", "U"}

    username = forms.CharField(min_length=8, max_length=32, validators=loginValidator)
    password = forms.CharField(min_length=8, max_length=32, validators=loginValidator)
    phone = forms.CharField(min_length=8, max_length=40, validators=phoneValidator)
    name = forms.CharField(min_length=8, max_length=40, validators=nameValidator)
    email = forms.CharField(min_length=8, max_length=40)
    license = forms.CharField(initial="00Z0-00000", min_length=8, max_length=10)
    role = forms.ChoiceField(choices=ROLES, initial="U")


class MatchResultListForm(forms.Form):
    team_id_list = SimpleArrayField(forms.CharField(min_length=3, max_length=6))
    goalscore = SimpleArrayField(forms.IntegerField())
    goalconceeded = SimpleArrayField(forms.IntegerField())


class MatchResultForm(forms.Form):
    goalscore = forms.IntegerField(required=True)
    goalconceeded = forms.IntegerField(required=True)
    hometeam = forms.CharField(min_length=8, max_length=20)
    awayteam = forms.CharField(min_length=8, max_length=20)
    home_goalscorer = forms.CharField(min_length=8, max_length=20)
    away_goalscorer = forms.CharField(min_length=8, max_length=20)
    home_yellowcard = forms.CharField(min_length=8, max_length=20)
    home_redcard = forms.CharField(min_length=8, max_length=20)
    league = forms.CharField(min_length=8, max_length=20)
    
