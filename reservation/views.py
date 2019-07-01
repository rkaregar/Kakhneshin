import re
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, TemplateView


class ReservationSearchView(TemplateView):
    template_name = 'reservation/search.html'

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        dates = re.split('/| - ', self.request.GET['daterange'])
        from_date = '-'.join([dates[2], dates[0], dates[1]])
        to_date = '-'.join([dates[5], dates[3], dates[4]])
        print('{}, {}'.format(from_date, to_date))
