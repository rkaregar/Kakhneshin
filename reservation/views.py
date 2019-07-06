import re
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from habitats.models import Habitat, GeographicDivision, RoomType
from reservation.forms import HabitatSearchForm


class ReservationSearchView(ListView):
    model = Habitat
    template_name = 'reservation/habitats-search.html'
    paginate_by = 10
    context_object_name = 'habitats'

    def get_queryset(self, **kwargs):
        self.form = HabitatSearchForm(self.request.GET)
        if self.form.is_valid():
            roomtypes = RoomType.objects.filter(capacity_in_person=self.form.cleaned_data['persons'],
                                                habitat__town_id=self.form.cleaned_data['division'])
            habitats = []
            for roomtype in roomtypes:
                if roomtype.habitat not in habitats and roomtype.has_empty_room(self.form.cleaned_data['from_date'],
                                                                                self.form.cleaned_data['to_date']):
                    habitats.append(roomtype.habitat)
            return habitats
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context
