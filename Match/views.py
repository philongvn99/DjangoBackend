from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.decorators import api_view
from common import support as sp, exceptions as exc

from . import forms

@api_view(["GET", "POST"])
def MatchForm(request):
    return HttpResponse(
        get_template("my_template.html")
            .render({
                'form' : forms.MatchResultForm(),
                'url_name': 'match'
            })
    )  