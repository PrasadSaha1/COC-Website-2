from . import views
from django.urls import path

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
    path("settings/", views.settings, name="settings"),
    path("change_username", views.change_username, name="change_username"),
    path("change_password", views.change_password, name="change_password"),
    path("logout_view", views.logout_view, name="logout_view"),
]
