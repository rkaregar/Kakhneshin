from datetime import datetime
import re
from datetime import datetime, date

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DetailView
from reservation.forms import ReservationForm
from reservation.models import Reservation

from habitats.models import Habitat, GeographicDivision, RoomType
from places.models import DistanceHabitatToPlace
from reservation.models import Reservation, ReservationComment, ReservationCommentPhoto, ReservationCommentVideo
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

        habitat = get_object_or_404(Habitat, pk=self.kwargs.get('habitat_pk', None))
        context['habitat'] = habitat
        context['distances'] = DistanceHabitatToPlace.objects.filter(
            habitat_id=self.kwargs.get('habitat_pk', None)).order_by('distance')
        context['reservations'] = Reservation.objects.filter(room__habitat=habitat,
                                                             member__user=self.request.user).order_by('-to_date')
        context['comments'] = ReservationComment.objects.filter(reservation__room__habitat=habitat).order_by(
            '-created_at')

        roomtypes = context['habitat'].roomtype_set.all()
        if 'persons' in self.request.GET:
            roomtypes = roomtypes.filter(capacity_in_person=self.request.GET['persons'])
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


class ReservationCommentView(LoginRequiredMixin, TemplateView):
    template_name = 'reservation/reservation_comment_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = get_object_or_404(Reservation, pk=self.kwargs.get('reservation_pk', None))
        context['reservation'] = reservation

        if self.request.user and reservation.member.user == self.request.user:
            if ReservationComment.objects.filter(reservation=reservation).exists():
                context['message'] = 'شما قبلا برای این رزرو نظر ثبت کرده‌اید'
        else:
            context['message'] = 'شما تنها می‌توانید برای رزروهای خود نظر ثبت کنید'

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        rating = request.POST.get('rating', None)
        if rating == '':
            rating = None
        review = request.POST.get('review', None)

        if not rating and not review:
            context['errors'] = ['ثبت حداقل یکی از موارد امتیاز یا متن نظر الزامیست']
        else:
            reservation = Reservation.objects.get(pk=self.kwargs.get('reservation_pk', None))
            reservation_comment = ReservationComment.objects.create(reservation=reservation, rating=rating,
                                                                    review=review)
            if self.request.FILES:
                for image in self.request.FILES.getlist('image'):
                    ReservationCommentPhoto.objects.create(reservation_comment=reservation_comment, photo=image)
                for video in self.request.FILES.getlist('video'):
                    ReservationCommentVideo.objects.create(reservation_comment=reservation_comment, video=video)

            context['message'] = 'نظر شما برای این رزرو با موفقیت ثبت شد'

        return self.render_to_response(context)


class ReservationListView(ListView):
    template_name = 'reservation/list.html'

    def get_queryset(self):
        return Reservation.objects.filter(member=self.request.user.member)


class ReservationCancelView(View):

    @staticmethod
    def post(request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if reservation.member.user.id != request.user.id:
            return HttpResponse(status=404)
        if reservation.cancel():
            messages.add_message(request, level=messages.INFO, message='رزرو با موفقیت لغو شد.')
        else:
            messages.add_message(request, level=messages.ERROR, message='لغو رزرو امکان پذیر نیست.')
        return redirect(reverse_lazy('reservation:list'))


class ReservationCreateView(CreateView):
    form_class = ReservationForm
    template_name = 'reservation/error.html'
    success_url = reverse_lazy('reservation:list')

    def get_form_kwargs(self):
        super_kwargs = super().get_form_kwargs()
        super_kwargs['member'] = self.request.user.member
        return super_kwargs

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'habitat_pk': self.kwargs.get('habitat_pk', None)})

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'رزرو با موفقیت انجام شد.')
        return super().form_valid(form)
