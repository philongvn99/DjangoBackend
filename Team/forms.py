
from django import forms

from .models import Team


class PlayerForm(forms.ModelForm):
    class Meta:
        model=Team
        fields="__all__"