import re
from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView
from reservation.forms import ReservationForm
from reservation.models import Reservation

from habitats.models import Habitat, GeographicDivision, RoomType
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


class ReservationHabitatView(TemplateView):
    template_name = 'reservation/habitat_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['habitat'] = get_object_or_404(Habitat, pk=kwargs.get('habitat_pk', None))

        context['form'] = {}
        context['form']['persons'] = self.request.GET.get('persons', None)
        context['form']['from_date'] = self.request.GET.get('from_date', None)
        context['form']['to_date'] = self.request.GET.get('to_date', None)
        context['form']['division'] = self.request.GET.get('division', None)

        roomtypes = context['habitat'].roomtype_set.all()
        if 'persons' in self.request.GET:
            roomtypes = roomtypes.filter(capacity_in_person=2)
        if 'from_date' and 'to_date' in self.request.GET:
            from_date = datetime.strptime(self.request.GET['from_date'], '%Y-%m-%d')
            to_date = datetime.strptime(self.request.GET['to_date'], '%Y-%m-%d')
            for roomtype in roomtypes:
                if not roomtype.has_empty_room(from_date,
                                               to_date):
                    roomtypes = roomtypes.exclude(pk=roomtype.pk)
            context['from_date'] = from_date.strftime('%m/%d/%Y')
            context['to_date'] = to_date.strftime('%m/%d/%Y')
        context['room_types'] = roomtypes.values()

        return context



class ReservationListView(ListView):

    template_name = 'reservation/list.html'

    def get_queryset(self):
        return Reservation.objects.filter(member=self.request.user.member)


class ReservationCreateView(CreateView):

    form_class = ReservationForm
    template_name = 'reservation/error.html'
    success_url = reverse_lazy('reservation:list')

    def get_form_kwargs(self):
        super_kwargs = super().get_form_kwargs()
        super_kwargs['member'] = self.request.user.member
        return super_kwargs

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


