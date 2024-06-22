from django.urls import path

from api.Team import views

urlpatterns = [
    path("", views.team, name="League Table"),
    path(
        "league/table/<int:league_id>/<int:season>",
        views.league_table,
        name="League Table by Season",
    ),
    path(
        "league/result/<str:date>", views.league_result, name="League Results from date"
    ),
]
