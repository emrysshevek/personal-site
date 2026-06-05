from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Collection


class IndexView(generic.ListView):
  template_name = "chooser/index.html"
  context_object_name = "collection_list"
  model = Collection

  # def get_queryset(self) -> QuerySet[Any]:
  #   """
  #   Return all collections
  #   """
  #   return Collection.objects.all()



class DetailView(generic.DetailView):
  model = Collection
  template_name = "chooser/detail.html"
  # TODO: filter collections to return only ones created by current user



def run(request, collection_id) -> HttpResponse:
  collection = get_object_or_404(Collection, pk=collection_id)
  
  return HttpResponse("future run page")



def choose(request, collection_id, tournament_id) -> HttpResponse:
  return HttpResponse("future choose page")