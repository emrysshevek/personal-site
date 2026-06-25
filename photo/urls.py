from django.urls import path

from photo.views import IndexView, GalleryView, PhotoView, ProjectView


app_name = "photo"
urlpatterns = [
  # ex: /photo/
  path("", IndexView.as_view(), name="index"),

  # ex: /photo/7
  path("<int:pk>", PhotoView.as_view(), name="photo"),

  # ex: /photo/gallery/
  path("gallery/", GalleryView.as_view(), name="gallery"),

  # ex: /photo/project/5
  path("project/<int:pk>/", ProjectView.as_view(), name="project"),

]