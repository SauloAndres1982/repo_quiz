from django.urls import path 
from .views import inicio, registro, loginView, logoutView, homeUsuario, jugar

urlpatterns = [
    path("", inicio, name="inicio"),
    path("login/", loginView, name="login"), 
    path("registro/", registro, name="registro"),
    path("logout/", logoutView, name="logout"),
    path("home/", homeUsuario, name="home"),
    path("jugar/", jugar, name="jugar")
]
