from django.urls import path, include
from . import views


urlpatterns = [
    path("player/", views.AllPlayerInfo, name="Player"),
    
    path("player/<int:ID>/", views.PlayerInfoByID, name="Info By ID"),
    path("player/<str:position>/", views.PlayerInfoByPosition, name="Info By Position"),
    
    path("league/table/", views.LeagueTable, name="League Table"),
    path("league/table/<int:season>/", views.LeagueTable, name="League Table by Season"),
    
    path("league/result/<str:date>/", views.LeagueResult, name="League Results from date"),

    path("user/login/", views.UserLogin, name="Log In"),
    path("user/signup/", views.UserRegister, name="Sign Up"),
    path("user/refresh/", views.UserRefreshToken, name="Refresh Token"),
    path("user/<str:username>/", views.UserInfo, name="User Info by Username"),
    
    path("test/", views.test, name="Info By ID"),
    path(r"api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
