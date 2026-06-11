from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def home(request):
  return render(request, "home/index.html", {"start": timezone.now})