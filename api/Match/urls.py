from django.urls import path

from api.Match import views

urlpatterns = [
    path(
        "<int:season>/<int:round>",
        views.league_result_by_round,
        name="League Res by round",
    ),
    path("<int:match_id>", views.match, name="Match Details"),
]
