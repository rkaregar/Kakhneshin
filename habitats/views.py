from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.shortcuts import render, get_object_or_404, redirect

from habitats.forms import CreateHabitatForm
from habitats.models import Habitat

from users.models import Member
import re


def all(request):
    raise NotImplementedError


class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')

    def post(self, request):
        dates = re.split('/| - ', request.POST['daterange'])
        from_date = '-'.join([dates[2], dates[0], dates[1]])
        to_date = '-'.join([dates[5], dates[3], dates[4]])
        # return redirect('/habitats/{}/{}'.format(from_date, to_date))  redirect to named url is also possible
        return render(request, 'homepage.html')


class HabitatCreateView(CreateView):
    form_class = CreateHabitatForm
    template_name = 'habitats/create_habitat.html'
    success_url = '/habitats/create'

    def form_valid(self, form):
        if not hasattr(self.request.user, 'member'):
            self.request.user.member, _ = Member.objects.get_or_create(user=self.request.user)

        form.instance.owner = self.request.user.member
        return super(HabitatCreateView, self).form_valid(form)


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
        return '/habitats/%s/update' % habitat_pk


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


class HabitatDetailView(View):
    def get(self, request, **kwargs):
        habitat = get_object_or_404(Habitat, pk=kwargs.get('habitat_pk', None))

        room_types = habitat.roomtype_set.all().values()
        return render(request, 'habitats/habitat_detail.html', {'habitat': habitat,
                                                                'room_types': room_types,
                                                                })
