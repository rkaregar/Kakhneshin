from django import forms
from habitats.models import Habitat


class CreateHabitatForm(forms.ModelForm):  # TODO: change name to HabitatForm
    class Meta:
        model = Habitat
        fields = ('name', 'address', 'town')
