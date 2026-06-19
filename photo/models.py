from django.db import models

from personalsite.storages import CustomS3Storage


class Photo(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=500)
  image = models.ImageField(upload_to="photos/", storage=CustomS3Storage())
