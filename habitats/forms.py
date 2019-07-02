from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django import forms
from django.core.exceptions import ValidationError

from habitats.models import Habitat, RoomType, RoomOutOfService


class CreateRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('type_name', 'capacity_in_person',
                  'cost_per_night', 'number_of_rooms_of_this_kind', 'has_breakfast', 'has_telephone',
                  'has_wifi', 'has_minibar', 'has_foreign_wc',
                  'has_bath_tub', 'has_shower', 'has_wc', 'details', 'photo')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        self.habitat = initial['habitat']
        super(CreateRoomTypeForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'

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


class CreateRoomOutOfServiceForm(forms.ModelForm):
    inclusive_since = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='تاریخ شروع')
    inclusive_until = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='تاریخ پایان')

    # def __init__(self, *args, **kwargs):
    #     super(CreateRoomOutOfServiceForm, self).__init__(*args, **kwargs)
    #     self.fields['room'].queryset = RoomType.objects.filter(habitat_id=kwargs['habitat_pk'])
    def form_valid(self, form):
        return super(CreateRoomOutOfServiceForm, self).form_valid(form)

    class Meta:
        model = RoomOutOfService
        fields = ('room', 'inclusive_since', 'inclusive_until', 'details')
