from django.contrib import admin

from .models import Collection, Item



class ItemInline(admin.TabularInline):
  model = Item
  extra = 1


class CollectionAdmin(admin.ModelAdmin):
  inlines = [ItemInline]


admin.site.register(Collection, CollectionAdmin)
