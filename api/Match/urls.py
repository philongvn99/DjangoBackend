from django.urls import path
from api.Match import views


urlpatterns = [
    path("form", views.match_form, name="MatchForm"),
]
