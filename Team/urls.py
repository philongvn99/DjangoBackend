from django.urls import path, include
from . import views


urlpatterns = [
    path("league/table", views.LeagueTable, name="League Table"),
    path("league/table/<int:season>", views.LeagueTable, name="League Table by Season"),
    path("league/result/<str:date>", views.LeagueResult, name="League Results from date"),
]
