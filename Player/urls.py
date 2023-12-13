from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.AllPlayerInfo, name="Player"),
    path("<int:ID>", views.PlayerInfoByID, name="Info By ID"),
    path("<str:position>", views.PlayerInfoByPosition, name="Info By Position"),
]
