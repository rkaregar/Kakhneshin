from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View

from habitats.models import GeographicDivision


class GeographicDivisionsSearchView(LoginRequiredMixin, View):
    def get(self, request):
        input = request.GET['value']
        if request.GET['only_cities'] == 'true':
            divisions = GeographicDivision.objects.filter(name__contains=input, is_city=True)
        else:
            divisions = GeographicDivision.objects.filter(name__contains=input)
        return JsonResponse(
            {'suggestions': [{"name": division.hierarchy_name, "pk": division.pk} for division in divisions],
             'word': input})
