from django.urls import path

from . import views

urlpatterns = [
    path("", views.Team, name="League Table"),
    path("league/table/<int:leagueId>/<int:season>", views.LeagueTable, name="League Table by Season"),
    path("league/result/<str:date>", views.LeagueResult, name="League Results from date"),
]
