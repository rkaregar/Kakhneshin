from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django import forms
from django.core.exceptions import ValidationError

from habitats.models import Habitat, RoomType, Room, RoomOutOfService


class CreateHabitatForm(forms.ModelForm):  # TODO: change name to HabitatForm
    class Meta:
        model = Habitat
        fields = ('name', 'address', 'town')


class CreateRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('type_name', 'capacity_in_person',
                  'cost_per_night', 'has_breakfast', 'has_telephone',
                  'has_wifi', 'has_minibar', 'has_foreign_wc',
                  'has_bath_tub', 'has_shower', 'has_wc', 'details')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        self.habitat = initial['habitat']
        super(CreateRoomTypeForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super(CreateRoomTypeForm, self).clean()
        qs = RoomType.objects.filter(habitat=self.habitat)
        if qs.filter(type_name=self.cleaned_data.get('type_name')).exists():
            raise ValidationError('نام انواع اتاق در هر اقامتگاه باید یکتا باشد.')
        self.cleaned_data['habitat'] = self.habitat
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.habitat = self.cleaned_data['habitat']
        return super(CreateRoomTypeForm, self).save(commit=commit)


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_type', 'number', 'details')


class CreateRoomOutOfServiceForm(forms.ModelForm):
    class Meta:
        model = RoomOutOfService
        fields = ('room', 'inclusive_since', 'inclusive_until', 'details')
