import re
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView
from reservation.forms import ReservationForm
from reservation.models import Reservation


class ReservationSearchView(TemplateView):
    template_name = 'reservation/search.html'

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        dates = re.split('/| - ', self.request.GET['daterange'])
        from_date = '-'.join([dates[2], dates[0], dates[1]])
        to_date = '-'.join([dates[5], dates[3], dates[4]])
        print('{}, {}'.format(from_date, to_date))



class ReservationListView(ListView):

    template_name = 'reservations/list.html'

    def get_queryset(self):
        return Reservation.objects.filter(member=self.request.user.member)


class ReservationUpdateView(UpdateView):

    form_class = ReservationForm
    template_name = 'reservations/change.html'

    def get_queryset(self):
        return Reservation.objects.filter(member=self.request.user.member)


class ReservationCreateView(CreateView):

    form_class = ReservationForm

    def get_form_kwargs(self):
        super_kwargs = super().get_form_kwargs()
        super_kwargs['member'] = self.request.user.member
        return super_kwargs

    def form_valid(self, form):
        super().form_valid(form)
        redirect('change', form.instance.id)
