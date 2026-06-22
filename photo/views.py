from django.shortcuts import render

from photo.models import Photo

# Create your views here.
def gallery(request):
  photos = Photo.objects.all()
  return render(request, "photo/gallery.html", {"photos": photos})
