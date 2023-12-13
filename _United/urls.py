from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("Auth.urls")),
    path("player/", include("Player.urls")),
    path("team/", include("Team.urls")),
    path("match/", include("Match.urls")),
]
