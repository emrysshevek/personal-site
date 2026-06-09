from django.urls import path

from . import views

app_name = "chooser"
urlpatterns = [
  # ex: /chooser/
  path("", views.IndexView.as_view(), name="index"),
  # ex: /chooser/5/
  path("<int:collection_id>/", views.detail, name="detail"),
  # ex: /chooser/5/run/
  path("run/<int:tournament_id>", views.run, name="run"),
  # ex: /run/3/choose
  path("run/<int:tournament_id>/choose", views.choose, name="choose"),
  # ex: /run/3/end
  path("run/<int:item_id>/end", views.end, name="end"),
]