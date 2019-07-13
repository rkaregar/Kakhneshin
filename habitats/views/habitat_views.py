from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from django.views.generic import View

from accounts.models import Transaction
from habitats.forms import HabitatStatForm
from habitats.models import Habitat
from places.models import Place, DistanceHabitatToPlace

import plotly as py
import plotly.graph_objs as go

import pandas as pd
from datetime import datetime


class HabitatCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Habitat
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'habitats/create_habitat.html'
    success_url = '/habitats'
    success_message = 'اقامتگاه %s با موفقیت ثبت شد!'

    def form_valid(self, form):
        form.instance.creator = self.request.user.member
        return super(HabitatCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')


# noinspection PyAttributeOutsideInit
class HabitatUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Habitat
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'habitats/update_habitat.html'
    success_message = 'اقامتگاه %s با موفقیت ویرایش شد!'

    def get_success_url(self):
        return '/habitats/%s/detail' % self.habitat_pk

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        return self.habitat

    def user_passed_test(self, request):
        if self.habitat.owner == self.request.user.member:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['town_name'] = self.habitat.town.name
        except Exception:
            context['town_name'] = ''
        return context

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.habitat is None:
            raise Http404
        if self.user_passed_test(request):
            return super(HabitatUpdateView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان ویرایش این اقامتگاه را ندارید')


# noinspection PyAttributeOutsideInit
class HabitatDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = '/habitats/'
    success_message = 'اقامتگاه %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        return self.habitat

    def user_passed_test(self, request):
        if self.habitat.owner == self.request.user.member:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.habitat is None:
            raise Http404
        if self.user_passed_test(request):
            return super(HabitatDeleteView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  حذف این اقامتگاه را ندارید')


class HabitatListView(ListView):
    model = Habitat

    def get_queryset(self):
        qs = super(HabitatListView, self).get_queryset()
        return qs.filter(owner=self.request.user.member)


class HabitatTinyDetailView(DetailView):
    template_name = 'habitats/habitat_detail_tiny.html'
    context_object_name = 'habitat'

    def get_object(self, queryset=None):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        return self.habitat

    def get_context_data(self, **kwargs):
        context = super(HabitatTinyDetailView, self).get_context_data(**kwargs)

        room_types = self.habitat.roomtype_set.all().values()
        context['room_types'] = room_types

        return context

    def user_passed_test(self, request):
        if self.habitat.owner == self.request.user.member:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.habitat is None:
            raise Http404
        if self.user_passed_test(request):
            return super(HabitatTinyDetailView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  دیدن جزییات این اقامتگاه را ندارید')


class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')


class HabitatStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'habitats/habitat_stat.html'

    def get_object(self, queryset=None):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        return self.habitat

    def get_context_data(self, **kwargs):
        context = super(HabitatStatsView, self).get_context_data(**kwargs)
        context['habitat'] = self.habitat
        owner = self.request.user
        self.form = HabitatStatForm(self.request.GET)
        from_date, to_date = timezone.datetime(
            year=2019, month=1,
            day=1), timezone.now()  # TODO set this to something reasonable when nothing is specified
        if self.form.is_valid():
            from_date = self.form.cleaned_data['from_date']
            to_date = self.form.cleaned_data['to_date']
        inputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date, to_user=owner,
                                                  verified=True).all()
        outputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date, from_user=owner,
                                                   verified=True).all()
        income = defaultdict(int)
        for im in inputs_money:
            income[im.created] += im.amount
        for im in outputs_money:
            income[im.creared] -= im.amount
        print(income)
        x = list(income.keys())
        y = list(income.values())
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="درآمد کل شما از این اقامتگاه", xaxis={'title': 'تاریخ'}, yaxis={'title': 'تومان'})
        figure = go.Figure(data=data, layout=layout)
        div = py.offline.plot(figure, auto_open=False, output_type='div')
        context['income_graph'] = div
        return context

    def user_passed_test(self, request):
        if self.habitat.owner == self.request.user.member:
            return True
        return False

    def get_object(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        return self.habitat

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.habitat is None:
            raise Http404
        if self.user_passed_test(request):
            return super(HabitatStatsView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  دیدن آمارهای این اقامتگاه را ندارید')


class DistanceToPlacesView(LoginRequiredMixin, TemplateView):
    template_name = 'habitats/distance_to_places.html'
    MAX_DISTANCES = 6

    def get_context_data(self, **kwargs):
        context = super(DistanceToPlacesView, self).get_context_data(**kwargs)

        habitat = Habitat.objects.get(pk=self.kwargs.get('habitat_pk', None))
        distances = DistanceHabitatToPlace.objects.filter(habitat=habitat).order_by('distance')
        places = Place.objects.filter(town=habitat.town).exclude(id__in=distances.values('place_id'))

        context['habitat'] = habitat
        context['distances'] = distances
        context['places'] = places

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        habitat = Habitat.objects.get(pk=self.kwargs.get('habitat_pk', None))

        if request.POST.get('delete', None):
            distance_id = request.POST.get('distance_id', None)
            DistanceHabitatToPlace.objects.get(pk=distance_id).delete()
        else:
            place_id = request.POST.get('place_id', None)
            distance = request.POST.get('distance', None)

            if DistanceHabitatToPlace.objects.filter(habitat=habitat, place_id=place_id).exists():
                context['errors'] = ['شما قبلا این مکان گردشگری را اضافه کرده‌اید']
            elif DistanceHabitatToPlace.objects.filter(habitat=habitat).count() < self.MAX_DISTANCES:
                DistanceHabitatToPlace.objects.create(place_id=place_id, habitat=habitat, distance=distance)
            else:
                context['errors'] = ['شما مجاز به اضافه کردن حداکثر {} مکان گردشگری هستید'.format(self.MAX_DISTANCES)]

        return self.render_to_response(context)
