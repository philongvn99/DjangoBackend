from django import forms

from api.Player.models import Player


class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"


class UpdatePlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            "kit_number",
            "salary",
            "height",
            "nationality",
            "role",
            "status",
            "avatar_link",
        ]
