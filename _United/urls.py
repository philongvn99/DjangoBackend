from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="admin/")),
    path("admin/", admin.site.urls),
    path("player/", include("api.Player.urls")),
    path("team/", include("api.Team.urls")),
    path("match/<int:league_id>/", include("api.Match.urls")),
    path("match/united/", include("api.UnitedMatch.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
