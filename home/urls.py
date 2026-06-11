from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
  # ex: /
  path("", views.home, name="index"),
  # ex: /about/
  path("about/", views.about, name="about"),
]