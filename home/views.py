from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from home.models import Project, ProjectSample


def home(request):
  projects = Project.objects.all()
  samples = ProjectSample.objects.all()
  return render(request, "home/index.html", {"projects": projects, "samples": samples})


def about(request):
  return render(request, "home/about.html")