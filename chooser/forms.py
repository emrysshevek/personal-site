from django import forms


class TournamentForm(forms.Form):
  num_players = forms.IntegerField(min_value=1, initial=1, label="number of players")
  method = forms.ChoiceField(choices=[("s", "simple"), ("t", "tournament")], widget=forms.RadioSelect, initial="t", label="Method", show_hidden_initial=True)
  weighting = forms.ChoiceField(choices=[("u", "uniform"), ("s", "seeded"), ("st", "strong"), ("w", "weak")], widget=forms.RadioSelect, initial="u", label="Weighting system")
  weight_strength = forms.IntegerField(min_value=1, max_value=4, initial=1, label="Weighting strength")
