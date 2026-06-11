from django.db import models


class Project(models.Model):
  name = models.CharField(max_length=200)
  url = models.URLField()
  description = models.CharField(max_length=500)

  def __str__(self) -> str:
    return self.name


class ProjectSample(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  url = models.URLField()
  description = models.CharField(max_length=500, default="")

