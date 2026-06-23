from django.db import models
from django.core.files.storage import FileSystemStorage

from personalsite import settings
from personalsite.storages import CustomS3Storage


class Photo(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=500)
  image = models.ImageField(upload_to="personal-site/photos/", storage=CustomS3Storage())
