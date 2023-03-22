from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/hello/", views.hello, name="hello"),
    path("UnitedHome/", include("United.urls")),
]
