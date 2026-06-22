from django.shortcuts import render

from photo.models import Photo

S3URL = "https://personal-bucket-058109276355-us-west-1-an.s3.us-west-1.amazonaws.com"

# Create your views here.
def gallery(request):
  photos = Photo.objects.all()
  return render(request, "photo/gallery.html", {"photos": photos, "s3_url": S3URL})
