from django.urls import path
from api.UnitedMatch import views


urlpatterns = [
    path("form", views.match_form, name="UnitedMatchForm"),
]
