from django.urls import path

from api.Team import views

urlpatterns = [
    path("", views.team, name="League Table"),
    path("league", views.league, name="League Table"),
    path(
        "league/table/<int:league_id>/<int:season>",
        views.league_table,
        name="League Table by Season",
    ),
]
