from django.urls import path

from photo.views import IndexView, GalleryView, ProjectView, photo_detail


app_name = "photo"
urlpatterns = [
  # ex: /photo/
  path("", IndexView.as_view(), name="index"),

  # ex: /photo/gallery/
  path("gallery/", GalleryView.as_view(), name="gallery"),

  # ex: /gallery/photos/6
  path("gallery/photos/<int:photo_id>/", photo_detail, name="gallery_photo"),

  # ex: /photo/project/5
  path("project/<int:pk>/", ProjectView.as_view(), name="project"),

  # ex: /photo/project/5/photos/3
  path("project/<int:project_id>/photos/<int:photo_id>/", photo_detail, name="photo"),

]