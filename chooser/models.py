import datetime
import random
import uuid

from django.utils import timezone
from django.db import models
import numpy as np


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
  lifespan = models.IntegerField(default=30)
  creation = models.DateTimeField(auto_now_add=True)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
  method = models.CharField(max_length=10, choices=[('simple', 'simple'), ('tournament', 'tournament')], default="tournament")
  weighting = models.CharField(max_length=10, choices=[('uniform', 'uniform'), ('seeded', 'seeded'), ('strong', 'strong'), ('weak', 'weak')], default="seed")
  strength = models.IntegerField(default=1)
  num_players = models.IntegerField(default=1)
  turn = models.IntegerField(default=0)
  final_choice = models.ForeignKey(Item, default=None, on_delete=models.CASCADE, null=True)
  ended = models.BooleanField(default=False)

  # objects = TournamentManager()

  def is_active(self):
    return not self.ended and timezone.now() - datetime.timedelta(minutes=self.lifespan) <= self.creation
  
  def get_remaining(self):
    return list(self.collection.item_set.all()) # type: ignore
  
  def get_options(self):
    remaining = self.get_remaining()
    counts_dict = {item: 0 for item in remaining}
    unique_counts_dict = {item: 0 for item in remaining}
    vetoed = set()

    preferences = [player.get_preferences() for player in self.player_set.all()] # type: ignore
    for item in remaining:
      if preferences.count(item) > self.num_players:
        return item

    for player in self.player_set.all():  # type: ignore
      for choice in player.choice_set.all():
        if choice.vetoed:
          vetoed.add(choice.item)
          remaining.remove(choice.item)
        else:
          counts_dict[choice.item] += 2 if player.turn_order == self.turn else 1

    if self.method == "simple" or len(remaining) == 1:
      return remaining
    
    if self.weighting == "random":
      return [remaining.pop(random.randrange(0, len(remaining))) for _ in range(2)]
    
    counts = np.array([counts_dict.get(item, 0) for item in remaining])
    weights = max(counts) - counts
    weights = np.pow(weights, self.strength)
    output = self.softmax(weights)

    if self.method == "weak":
      return np.random.choice(remaining, 2, replace=False, p=output).tolist()
    elif self.method == "strong":
      output = 1 - output
      return np.random.choice(remaining, 2, replace=False, p=output).tolist()
    else:
      idx = np.random.choice(len(remaining), p=output)
      opt1 = remaining.pop(idx)
      counts = np.array([counts_dict[item] for item in remaining])
      weights = np.pow(counts, self.strength)
      output = self.softmax(weights)
      opt2 = np.random.choice(remaining, p=output)
      return [opt1, opt2]
      
  def softmax(self, array):
    e_x = np.exp(array - np.max(array))
    return e_x / e_x.sum()
  
  def get_current_player(self):
    return self.player_set.get(turn_order=self.turn) # type: ignore

  def __str__(self) -> str:
    return super().__str__()


class Player(models.Model):
  name = models.CharField(max_length=200)
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  turn_order = models.SmallIntegerField(default=0)

  def did_veto(self, item):
    return any([choice.vetoed for choice in self.choice_set.all() if choice.item == item]) # type: ignore
  
  def get_preferences(self):
    return set([choice.item for choice in self.choice_set.all() if not self.did_veto(choice.item)]) # type: ignore

  def __str__(self) -> str:
    return self.name


class Choice(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  vetoed = models.BooleanField()

  def __str__(self) -> str:
    return f"{self.item}: {"vetoed" if self.vetoed else "chosen"} by player {self.player}"
  

