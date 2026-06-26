import os

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic

from home.models import Project
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


def photo_detail(request, photo_id, project_id=-1):
  photo = get_object_or_404(Photo, pk=photo_id)
  
  if project_id == -1:
    photo_ids = [p.id for p in Photo.objects.all()] # type: ignore
  else:
    photo_ids = [p.id for p in get_object_or_404(Project, pk=project_id).photo_set.all()] # type: ignore
  
  idx = photo_ids.index(photo.id) # type: ignore
  next = photo_ids[idx + 1] if idx < len(photo_ids) - 1 else None
  prev = photo_ids[idx - 1] if idx > 0 else None
  print(photo_ids, idx, next, prev)
  context = {
    "photo": photo,
    "url_root":  os.path.normpath(os.path.join(request.path, "../")),
    "show_next": next is not None,
    "show_prev": prev is not None,
    "next": next,
    "prev": prev,
  }

  return render(request, "photo/photo.html", context=context)