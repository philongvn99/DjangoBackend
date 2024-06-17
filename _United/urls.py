from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='admin/')),
    path("admin/", admin.site.urls),
    path("player/", include("api.Player.urls")),
    path("team/", include("api.Team.urls")),
    path("match/", include("api.Match.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
