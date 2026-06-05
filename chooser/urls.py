from django.urls import path

from . import views

app_name = "chooser"
urlpatterns = [
  # ex: /chooser/
  path("", views.IndexView.as_view(), name="index"),
  # ex: /chooser/5/
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  # # ex: /chooser/5/run/
  path("<int:collection_id>/run/", views.run, name="run"),
  # # ex: /polls/5/run/3/choose
  path("<int:collection_id>/run/<int:tournament_id>/choose", views.choose, name="choose"),
]