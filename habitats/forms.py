from django import forms
from habitats.models import Habitat, RoomType, Room, RoomOutOfService


class CreateHabitatForm(forms.ModelForm):  # TODO: change name to HabitatForm
    class Meta:
        model = Habitat
        fields = ('name', 'address', 'town')


class CreateRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('habitat', 'type_name', 'capacity_in_person',
                  'cost_per_night', 'has_breakfast', 'has_telephone',
                  'has_wifi', 'has_minibar', 'has_foreign_wc',
                  'has_bath_tub', 'has_shower', 'has_wc', 'details')


class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_type', 'number', 'details')


class CreateRoomOutOfService(forms.ModelForm):
    class Meta:
        model = RoomOutOfService
        fields = ('room', 'inclusive_since', 'inclusive_until', 'details')
