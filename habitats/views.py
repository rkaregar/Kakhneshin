from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from habitats.forms import CreateHabitatForm
from habitats.models import Habitat


def all(request):
    raise NotImplementedError


class HabitatCreateView(CreateView):
    form_class = CreateHabitatForm
    template_name = 'habitats/create_habitat.html'
    success_url = '/habitats/create'


class HabitatUpdateView(UpdateView):
    form_class = CreateHabitatForm
    template_name = 'habitats/update_habitat.html'
    success_url = '/habitats/update'

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        habitat_pk = self.get_habitat_pk()
        return Habitat.objects.get(pk=habitat_pk)

    def get_success_url(self):
        habitat_pk = self.get_habitat_pk()
        return '/habitats/%s/update' % habitat_pk;


class HabitatDeleteView(DeleteView):
    success_url = '/habitats/'

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        habitat_pk = self.get_habitat_pk()
        return Habitat.objects.get(pk=habitat_pk)


class HabitatListView(ListView):
    model = Habitat
