from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from habitats.models import Habitat, GeographicDivision, RoomType
from places.models import DistanceHabitatToPlace
from reservation.forms import HabitatSearchForm


class ReservationSearchView(ListView):
    model = Habitat
    template_name = 'reservation/habitats-search.html'
    # paginate_by = 10 TODO
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
        try:
            context['division_name'] = GeographicDivision.objects.get(
                pk=self.form.cleaned_data['division']).hierarchy_name
        except Exception:
            context['division_name'] = ''
        return context


class ReservationHabitatView(ListView):
    model = RoomType
    template_name = 'reservation/habitat_detail.html'
    context_object_name = 'room_types'

    def get_queryset(self, **kwargs):
        self.form = HabitatSearchForm(self.request.GET)
        if self.form.is_valid():
            habitat = get_object_or_404(Habitat, pk=self.kwargs.get('habitat_pk', None))
            roomtypes = habitat.roomtype_set.all()
            if 'persons' in self.request.GET:
                roomtypes = roomtypes.filter(capacity_in_person=self.request.GET['persons'])
            if 'from_date' and 'to_date' in self.request.GET:
                for roomtype in roomtypes:
                    if not roomtype.has_empty_room(datetime.strptime(self.request.GET['from_date'], '%Y-%m-%d'),
                                                   datetime.strptime(self.request.GET['to_date'], '%Y-%m-%d')):
                        roomtypes = roomtypes.exclude(pk=roomtype.pk)
            return roomtypes.values()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.form
        try:
            context['division_name'] = GeographicDivision.objects.get(
                pk=self.form.cleaned_data['division']).hierarchy_name
        except Exception:
            context['division_name'] = ''

        context['habitat'] = get_object_or_404(Habitat, pk=self.kwargs.get('habitat_pk', None))
        context['distances'] = DistanceHabitatToPlace.objects.filter(
            habitat_id=self.kwargs.get('habitat_pk', None)).order_by('distance')

        return context
