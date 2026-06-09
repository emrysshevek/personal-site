from django.contrib import admin

from .models import Collection, Item, Player, Tournament



class ItemInline(admin.TabularInline):
  model = Item
  extra = 1


class CollectionAdmin(admin.ModelAdmin):
  inlines = [ItemInline]


class PlayerInline(admin.StackedInline):
  model = Player


class TournamentAdmin(admin.ModelAdmin):
  inlines = [PlayerInline]


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Tournament, TournamentAdmin)
