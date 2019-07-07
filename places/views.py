from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from places.models import Place


class PlaceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Place
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'places/create_place.html'
    success_url = '/places'
    success_message = 'مکان دیدنی %s با موفقیت ثبت شد!'

    def form_valid(self, form):
        form.instance.owner = self.request.user.member
        return super(PlaceCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')


# noinspection PyAttributeOutsideInit
class PlaceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Place
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'places/update_place.html'
    success_message = 'مکان دیدنی %s با موفقیت ویرایش شد!'

    def get_success_url(self):
        return '/places/%s/detail' % self.place_pk

    def get_success_message(self, cleaned_data):
        print(cleaned_data.get('name'))
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)
        return self.place

    def user_passed_test(self, request):
        return request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['town_name'] = self.place.town.name
        except Exception:
            context['town_name'] = ''
        return context

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceUpdateView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان ویرایش این مکان دیدنی را ندارید')


# noinspection PyAttributeOutsideInit
class PlaceDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = '/places/'
    success_message = 'مکان دیدنی %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        print(cleaned_data.get('name'))
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)
        return self.place

    def user_passed_test(self, request):
        return request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceDeleteView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  حذف این مکان دیدنی را ندارید')


class PlaceListView(ListView):
    model = Place


class PlaceTinyDetailView(DetailView):
    template_name = 'places/place_detail_tiny.html'
    context_object_name = 'place'

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)
        return self.place

    def user_passed_test(self, request):
        return request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceTinyDetailView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  دیدن جزییات این مکان دیدنی را ندارید')

