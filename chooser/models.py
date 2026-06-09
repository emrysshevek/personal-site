import datetime
import random
import uuid

from django.utils import timezone
from django.db import models


class Collection(models.Model):
  name = models.CharField(max_length=200)
  max_history = models.IntegerField(default=5)

  def __str__(self) -> str:
    return self.name


class Item(models.Model):
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
  value = models.CharField(max_length=200)
  times_picked = models.IntegerField(default=0)
  last_picked = models.DateTimeField("date last picked")

  def __str__(self) -> str:
    return self.value
  

class TournamentManager(models.Manager):
  def get_queryset(self) -> models.QuerySet:
    return super().get_queryset().filter(ended=False, creation__gte=(timezone.now() - datetime.timedelta(minutes=30)))


class Tournament(models.Model):
  # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
  lifespan = models.IntegerField(default=30)
  creation = models.DateTimeField(auto_now_add=True)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
  num_players = models.IntegerField(default=1)
  turn = models.IntegerField(default=0)
  final_choice = models.ForeignKey(Item, default=None, on_delete=models.CASCADE, null=True)
  ended = models.BooleanField(default=False)

  # objects = TournamentManager()

  def is_active(self):
    return not self.ended and timezone.now() - datetime.timedelta(minutes=self.lifespan) <= self.creation
  
  def get_options(self):
    remaining = list(self.collection.item_set.all()) # type: ignore

    for player in self.player_set.all():  # type: ignore
      for choice in player.choice_set.all():
        if choice.vetoed:
          remaining.remove(choice.item)

    if len(remaining) == 1:
      return remaining
    else:
      return [remaining.pop(random.randrange(0, len(remaining))) for _ in range(2)]
  
  def get_current_player(self):
    return self.player_set.get(turn_order=self.turn) # type: ignore

  def __str__(self) -> str:
    return super().__str__()


class Player(models.Model):
  name = models.CharField(max_length=200)
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  turn_order = models.SmallIntegerField(default=0)

  def __str__(self) -> str:
    return self.name


class Choice(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  vetoed = models.BooleanField()

  def __str__(self) -> str:
    return f"{self.item}: {"vetoed" if self.vetoed else "chosen"} by player {self.player}"
  

