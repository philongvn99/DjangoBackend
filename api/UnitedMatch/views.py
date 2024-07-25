from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.decorators import api_view

from api.Match import forms


@api_view(["GET", "POST"])
def match_form(_):
    return HttpResponse(
        get_template("my_template.html").render(
            {"form": forms.LeagueMatchForm(), "url_name": "match"}
        )
    )
