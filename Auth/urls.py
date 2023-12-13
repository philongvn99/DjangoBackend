from django.urls import path, include
from . import views


urlpatterns = [
    path("login", views.UserLogin, name="Log In"),
    path("signup", views.UserRegister, name="Sign Up"),
    path("<str:username>", views.UserInfo, name="User Info by Username"),
]
