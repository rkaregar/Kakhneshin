import re
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from habitats.models import Habitat, GeographicDivision


class ReservationSearchView(ListView):
    model = Habitat
    template_name = 'reservation/search.html'
    paginate_by = 10
    context_object_name = 'habitats'

    def get_queryset(self, **kwargs):
        habitats = Habitat.objects.all()
        if 'division' in self.request.GET:
            habitats = habitats.filter(town=GeographicDivision.objects.get(pk=self.request.GET['division']))
        # dates = re.split('/| - ', self.request.GET['daterange'])
        # from_date = '-'.join([dates[2], dates[0], dates[1]])
        # to_date = '-'.join([dates[5], dates[3], dates[4]])
        return habitats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['division'] = {'name': '', 'value': ''}
