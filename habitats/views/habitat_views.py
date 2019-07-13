from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from django.views.generic import View

from habitats.models import Habitat
from places.models import Place, DistanceHabitatToPlace


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
