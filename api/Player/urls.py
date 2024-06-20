from django.urls import path

from api.Player import views

urlpatterns = [
    path("", views.all_player, name="Player"),
    path("<int:ID>", views.player_by_id, name="Info By ID"),
    path("<str:position>", views.player_by_position, name="Info By Position"),
]
