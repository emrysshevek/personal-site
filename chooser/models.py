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


class Tournament(models.Model):
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE)


class Player(models.Model):
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  choices = models.ManyToManyField(Item, verbose_name=_(""))
