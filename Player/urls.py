from django.urls import path

from . import views

urlpatterns = [
    path("", views.AllPlayer, name="Player"),
    path("<int:ID>", views.PlayerByID, name="Info By ID"),
    path("<str:position>", views.PlayerByPosition, name="Info By Position"),
]
