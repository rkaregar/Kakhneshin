from collections import defaultdict
from typing import Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from django.views.generic import View

from accounts.models import Transaction
from habitats.forms import HabitatStatForm
from habitats.models import Habitat, RoomType, GeographicDivision
from places.models import Place, DistanceHabitatToPlace
from reservation.models import Reservation, ReservationComment, Reservation

import plotly as py
import plotly.graph_objs as go


# from django.utils.timezone import timedelta


class HabitatCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Habitat
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'habitats/create_habitat.html'
    success_url = '/habitats'
    success_message = 'اقامتگاه %s با موفقیت ثبت شد!'

    def form_valid(self, form):
        form.instance.owner = self.request.user.member
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

        habitat = Habitat.objects.get(pk=self.kwargs.get('habitat_pk', None))
        if not habitat.confirm:
            context['errors'] = [
                'این اقامتگاه هنوز توسط مدیر سامانه تایید نشده است، به همین دلیل به کاربران نشان داده نخواهد شد.', ]
        room_types = habitat.roomtype_set.all().values()

        context['room_types'] = room_types
        context['reservations'] = Reservation.objects.filter(room__habitat=habitat).order_by('-to_date')
        context['comments'] = ReservationComment.objects.filter(reservation__room__habitat=habitat).order_by(
            '-created_at')
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

    @staticmethod
    def to_unix_time(dt):
        epoch = timezone.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000

    def get_input_moneys(self, from_date, to_date) -> Dict:
        owner = self.request.user
        inputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date, to_user=owner,
                                                  fee_reservations__isnull=False,
                                                  fee_reservations__room__habitat=self.habitat, verified=True).all()
        income = defaultdict(int)

        for day in [from_date + timezone.timedelta(i) for i in range((to_date - from_date).days + 1)]:
            income[day.replace(hour=0, minute=0, second=0, microsecond=0)] = 0

        for im in inputs_money.all():
            created = im.created
            income[created.replace(hour=0, minute=0, second=0, microsecond=0)] += im.amount
        return income

    def get_income_graph(self, from_date, to_date):
        income = self.get_input_moneys(from_date, to_date)
        x = list(income.keys())
        y = list(income.values())
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 100},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="نمودار درآمد روزانه‌ی شما از این اقامتگاه", xaxis={'title': 'تاریخ'},
                           yaxis={'title': 'تومان'})
        figure = go.Figure(data=data, layout=layout)
        div = py.offline.plot(figure, auto_open=False, output_type='div')
        return div

    def get_context_data(self, **kwargs):
        context = super(HabitatStatsView, self).get_context_data(**kwargs)
        context['habitat'] = self.habitat
        owner = self.request.user
        self.form = HabitatStatForm(self.request.GET)
        from_date, to_date = timezone.now() - timezone.timedelta(days=90), timezone.now()
        if self.form.is_valid():
            from_date = self.form.cleaned_data['from_date']
            to_date = self.form.cleaned_data['to_date']
        context['income_graph'] = self.get_income_graph(from_date, to_date)

        ready_room_types = defaultdict(int)
        disabled_room_types = defaultdict(int)
        reserved_room_types = defaultdict(int)
        room_types = {}
        for room_type in self.habitat.roomtype_set.all():  # type: RoomType
            num_of_disabled_today = room_type.get_out_of_service_rooms_count_list(timezone.now(),
                                                                                  timezone.now() + timezone.timedelta(
                                                                                      days=1))[0]
            num_of_reserved_today = room_type.get_reserved_rooms_count_list(timezone.now(),
                                                                            timezone.now() + timezone.timedelta(
                                                                                days=1))[0]
            disabled_room_types[room_type.type_name] = num_of_disabled_today
            reserved_room_types[room_type.type_name] = num_of_reserved_today
            ready_room_types[
                room_type.type_name] = room_type.number_of_rooms_of_this_kind - num_of_reserved_today - num_of_disabled_today
            room_types[room_type.type_name] = room_type.get_reserve_ready_out_count_list(timezone.now(),
                                                                                         timezone.now() + timezone.timedelta(
                                                                                             days=30))

        ready_rooms_trace = go.Bar(x=list(ready_room_types.keys()), y=list(ready_room_types.values()),
                                   name='آماده برای رزرو شدن')
        disabled_rooms_trace = go.Bar(x=list(disabled_room_types.keys()), y=list(disabled_room_types.values()),
                                      name='خارج از سرویس')
        in_use_rooms_trace = go.Bar(x=list(reserved_room_types.keys()), y=list(reserved_room_types.values()),
                                    name='رزرو '
                                         'شده')
        rooms_data = [ready_rooms_trace, disabled_rooms_trace, in_use_rooms_trace]
        stack_bar_layout = go.Layout(
            title='نمودار وضعیت انواع اتاق‌‌های شما امروز'
            , barmode='stack'
        )
        rooms_fig = go.Figure(data=rooms_data, layout=stack_bar_layout)
        rooms_div = py.offline.plot(rooms_fig, auto_open=False, output_type='div')
        context['rooms_graph'] = rooms_div
        dates = [timezone.now() + timezone.timedelta(i) for i in range(30)]
        rooms_time_data = []
        for type_name, reserved_ready_out_list in room_types.items():
            reserveds, readys, outs = [], [], []
            for res, rea, out in reserved_ready_out_list:
                reserveds.append(res)
                readys.append(rea)
                outs.append(out)
            trace_res = go.Scatter(x=dates, y=reserveds, name=type_name + ' ' + ' رزرو شده')
            trace_rea = go.Scatter(x=dates, y=readys, name=type_name + ' ' + 'آماده‌')
            trace_out = go.Scatter(x=dates, y=outs, name=type_name + ' ' + 'خارج از سرویس')
            rooms_time_data += [trace_res, trace_rea, trace_out]
        layout = dict(
            title='نمودار وضعیت اتاق‌های شما در هر روز',
            xaxis=dict(
                range=[dates[0], dates[-1]],
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='یک ماه اخیر',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='۶ ماه اخیر',
                             step='month',
                             stepmode='backward'),
                        dict(step='all'
                             , label='کل'
                             )
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.Figure(data=rooms_time_data, layout=layout)
        fig.update_xaxes(title_font=dict(size=40, family='Courier', color='crimson'))
        rooms_time_graph = py.offline.plot(fig, auto_open=False, output_type='div')
        context['rooms_time_graph'] = rooms_time_graph

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


class HabitatManagementStatsView(HabitatStatsView):

    def get_input_moneys(self, from_date, to_date) -> Dict:
        owner = self.request.user
        inputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date, to_user=None,
                                                  reservations__isnull=False, reservations__room__habitat=self.habitat,
                                                  verified=True).all()
        output_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date,
                                                  to_user=self.habitat.owner.user,
                                                  fee_reservations__isnull=False,
                                                  fee_reservations__room__habitat=self.habitat, verified=True).all()
        income = defaultdict(int)
        for im in inputs_money.all():
            created = im.created
            income[created.replace(hour=0, second=0, microsecond=0)] += im.amount
        for im in output_money.all():
            created = im.created
            income[created.replace(hour=0, second=0, microsecond=0)] -= im.amount
        return income

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied('شما مدیر سامانه نیستید.')
        return super(HabitatManagementStatsView, self).dispatch(*args, **kwargs)


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


class HabitatAllStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'habitats/habitat_all_stats.html'

    @staticmethod
    def to_unix_time(dt):
        epoch = timezone.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000

    def get_reservations_query_set(self):
        return Reservation.objects.filter(room__habitat__owner=self.request.user.member)

    def get_habitats_query_set(self):
        return Habitat.objects.filter(owner=self.request.user.member)

    def get_income(self, from_date, to_date):
        member = self.request.user.member
        outputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date,
                                                   fee_reservations__isnull=False,
                                                   fee_reservations__room__habitat__owner=member,
                                                   verified=True).all()
        income = defaultdict(int)
        for im in outputs_money.all():
            print(im.created)
            income[im.created.replace(hour=0, second=0, microsecond=0)] += im.amount
        return income

    def get_context_data(self, **kwargs):
        context = super(HabitatAllStatsView, self).get_context_data(**kwargs)
        self.form = HabitatStatForm(self.request.GET)
        from_date, to_date = timezone.datetime(
            year=2019, month=1,
            day=1), timezone.now()
        if self.form.is_valid():
            from_date = self.form.cleaned_data['from_date']
            to_date = self.form.cleaned_data['to_date']
        income = self.get_income(from_date, to_date)
        print(income)
        x = list(income.keys())
        print(x)
        y = list(income.values())
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = dict(
            title='درآمد روزانه‌ی شما از اقامتگاه‌هایتان',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date',
                title='تاریخ',
            ),
            yaxis=dict(
                title='درآمد'
            )
        )
        figure = go.Figure(data=data, layout=layout)
        div = py.offline.plot(figure, auto_open=False, output_type='div')
        context['income_graph'] = div

        selected_habitats = self.get_habitats_query_set()
        confirmed_habitats = Habitat.objects.filter(confirm=True).count()
        not_confirmed_habitats = Habitat.objects.count() - confirmed_habitats
        habitats_stat_data = go.Pie(labels=['فعال', 'غیرفعال'], values=[confirmed_habitats, not_confirmed_habitats],
                                    hoverinfo='label+value')
        figure = go.Figure(data=[habitats_stat_data])
        div = py.offline.plot(figure, auto_open=False, output_type='div')
        context['confirmed_graph'] = div

        selected_reservations = self.get_reservations_query_set()
        reserved = selected_reservations.filter(is_active=True).count()
        cancelled = selected_reservations.filter(is_active=False).count()
        reserve_data = go.Pie(labels=['انجام‌شده', 'لغو شده'], values=[reserved, cancelled],
                              hoverinfo='label+value')
        figure = go.Figure(data=[reserve_data])
        div = py.offline.plot(figure, auto_open=False, output_type='div')
        context['reserve_graph'] = div

        context['habitats'] = Habitat.objects.filter(owner=self.request.user.member).all()

        return context


class DivisionStat:
    def __init__(self, division):
        self.division = division

    def get_habitats(self):
        habitats = set()
        for habitat in Habitat.objects.all():
            father_ids = [father.id for father in habitat.town.get_fathers]
            if self.division.id == habitat.town.id or self.division.id in father_ids:
                habitats.add(habitat)
        return habitats

    def empty_rooms_count(self):
        contained_habitats = list(self.get_habitats())
        today = timezone.now()
        return sum([habitat.get_reserve_ready_out(today)[1] for habitat in contained_habitats])


class HabitatAllManagementStatsView(HabitatAllStatsView):
    template_name = 'habitats/habitat_all_management_stats.html'

    def get_reservations_query_set(self):
        return Reservation.objects

    def get_habitats_query_set(self):
        return Habitat.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(HabitatAllManagementStatsView, self).get_context_data(**kwargs)
        context['province_table'] = [DivisionStat(province) for province in GeographicDivision.get_all_provinces()]
        return context

    def get_income(self, from_date, to_date):
        inputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date,
                                                  verified=True,
                                                  reservations__isnull=False).all()
        outputs_money = Transaction.objects.filter(created__gte=from_date, created__lte=to_date,
                                                   fee_reservations__isnull=False, verified=True).all()
        income = defaultdict(int)
        for im in inputs_money.all():
            income[im.created.replace(hour=0, second=0, microsecond=0)] += im.amount
        for im in outputs_money.all():
            print(im.created)
            income[im.created.replace(hour=0, second=0, microsecond=0)] -= im.amount
        return income


class HabitatDivisionStatsView(TemplateView):
    template_name = 'habitats/habitat_division_stats.html'

    def get_context_data(self, **kwargs):
        context = super(HabitatDivisionStatsView, self).get_context_data(**kwargs)
        context['town_table'] = [DivisionStat(town) for town in self.childs]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.division_pk = kwargs.pop('division_pk')
        self.division = GeographicDivision.objects.filter(pk=self.division_pk)
        self.childs = GeographicDivision.get_childs(self.division_pk)
        return super(HabitatDivisionStatsView, self).dispatch(request, *args, **kwargs)


class HabitatTownStatsView(TemplateView):
    template_name = 'habitats/habitat_town_stats.html'

    def get_context_data(self, **kwargs):
        context = super(HabitatTownStatsView, self).get_context_data(**kwargs)
        context['habitats'] = Habitat.objects.filter(town_id=self.town_pk).all()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.town_pk = kwargs.pop('town_pk')
        self.town = GeographicDivision.objects.filter(pk=self.town_pk)
        print(self.town_pk, 'khar')
        return super(HabitatTownStatsView, self).dispatch(request, *args, **kwargs)
