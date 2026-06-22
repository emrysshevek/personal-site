from typing import Any

from django.db.models.query import F, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Collection, Item, Tournament, Player
from .forms import TournamentForm


class IndexView(generic.ListView):
  template_name = "chooser/index.html"
  context_object_name = "collection_list"
  model = Collection


# class DetailView(generic.DetailView):
#   model = Collection
#   template_name = "chooser/detail.html"


def detail(request, collection_id) -> HttpResponse:

  if request.method == "POST":
    print(f"Creating tournament based on form data")
    form = TournamentForm(request.POST)
    if form.is_valid():
      t = Tournament()
      t.collection = Collection.objects.get(pk=collection_id)
      t.num_players = form.cleaned_data["num_players"]
      t.method = form.cleaned_data["method"]
      t.weighting = form.cleaned_data["weighting"]
      t.strength = form.cleaned_data["weight_strength"]
      t.save()
      for i in range(form.cleaned_data["num_players"]):
        player = Player()
        player.name = f"Player {i+1}"
        player.tournament = t
        player.turn_order = i
        player.save()
      return HttpResponseRedirect(reverse("chooser:run", args=(t.id,))) # type: ignore
  else:
    form = TournamentForm()

  collection = Collection.objects.get(pk=collection_id)
  return render(request, "chooser/detail.html", {"form": form, "collection": collection})



def run(request, tournament_id) -> HttpResponse:
  tournament =  get_object_or_404(Tournament, id=tournament_id)
  options = tournament.get_options()
  if len(options) == 1:
    return HttpResponseRedirect(reverse("chooser:end", args=(options[0].id,)))
  else:
    return render(request, "chooser/run.html", {"tournament": tournament})



def choose(request, tournament_id) -> HttpResponse:
  tournament = get_object_or_404(Tournament, pk=tournament_id)
  if 'pass' in request.POST:
    tournament.turn = (F("turn") + 1) % tournament.num_players
    tournament.save()
    return HttpResponseRedirect(
      reverse("chooser:run", args=(tournament.id,)) # type: ignore
    )

  try:
    selected_item = tournament.collection.item_set.get(pk=request.POST["item"]) # type: ignore
  except:
    # Redisplay the item selection form
    return render(
      request,
      "chooser/run.html",
      {
        "tournament": tournament,
        "error_message": "You didn't select a item"
      },
    )
  
  Choice(
    item=selected_item,
    player=tournament.get_current_player(),
    vetoed='eliminate' in request.POST,
  ).save()

  tournament.turn = (F("turn") + 1) % tournament.num_players
  tournament.save()

  return HttpResponseRedirect(
    reverse("chooser:run", args=(tournament.id,)) # type: ignore
  )

def end(request, item_id):
  item = get_object_or_404(Item, pk=item_id)
  return render(request, "chooser/end.html", {"item": item})