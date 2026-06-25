from django.shortcuts import render
from django.views import generic

from photo.models import Photo, PhotoProject


class IndexView(generic.ListView):
  template_name = "photo/index.html"
  context_object_name = "projects"
  model = PhotoProject
  

class GalleryView(generic.ListView):
  template_name = "photo/gallery.html"
  context_object_name = "photos"
  model = Photo


class ProjectView(generic.DetailView):
  template_name = "photo/project.html"
  context_object_name = "project"
  model = PhotoProject


class PhotoView(generic.DetailView):
  template_name = "photo/photo.html"
  context_object_name = "photo"
  model = Photo

  

  
# def gallery(request):
#   photos = Photo.objects.all()
#   return render(request, "photo/gallery.html", {"photos": photos})
