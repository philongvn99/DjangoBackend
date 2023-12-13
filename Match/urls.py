from django.urls import path
from . import views


urlpatterns = [
    path("form", views.MatchForm, name="MatchForm"),
]
