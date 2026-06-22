from django.urls import path

from . import views

app_name = "photo"
urlpatterns = [
  # ex: /photo/
  path("", views.gallery, name="index"),
]