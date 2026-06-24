from django.urls import path

from photo.views import IndexView, GalleryView

from . import views

app_name = "photo"
urlpatterns = [
  # ex: /photo/
  path("", IndexView.as_view(), name="index"),

  # ex: /photo/gallery/
  path("gallery/", GalleryView.as_view(), name="gallery"),
]