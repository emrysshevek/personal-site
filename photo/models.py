from django.db import models
from django.core.files.storage import FileSystemStorage

from personalsite import settings
from personalsite.storages import CustomS3Storage


class PhotoProject(models.Model):
  title = models.CharField(max_length=100, blank=True)
  statement = models.CharField(max_length=1000, blank=True)
  summary = models.CharField(max_length=500, blank=True)

  def __str__(self) -> str:
    return self.title


class Photo(models.Model):
  title = models.CharField(max_length=100, blank=True, unique=True, null=True)
  description = models.CharField(max_length=500, blank=True)
  # image = models.ImageField(upload_to="photos/", storage=CustomS3Storage())
  image = models.ImageField(upload_to="photos/")
  project = models.ForeignKey(PhotoProject, on_delete=models.DO_NOTHING, blank=True, null=True)

  def __str__(self) -> str:
    return self.title or "Placeholder Title" + str(self.id) # type: ignore
  

