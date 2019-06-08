import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View

from habitats.models import Habitat


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
        print(cleaned_data.get('name'))
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
            return super(HabitatUpdateView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان ویرایش این اقامتگاه را ندارید')


# noinspection PyAttributeOutsideInit
class HabitatDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = '/habitats/'
    success_message = 'اقامتگاه %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        print(cleaned_data.get('name'))
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
            return super(HabitatTinyDetailView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  دیدن جزییات این اقامتگاه را ندارید')


class HabitatDetailView(View):
    def get(self, request, **kwargs):
        habitat = get_object_or_404(Habitat, pk=kwargs.get('habitat_pk', None))

        room_types = habitat.roomtype_set.all().values()
        return render(request, 'habitats/habitat_detail.html', {'habitat': habitat,
                                                                'room_types': room_types,
                                                                })


class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')

    def post(self, request):
        dates = re.split('/| - ', request.POST['daterange'])
        from_date = '-'.join([dates[2], dates[0], dates[1]])
        to_date = '-'.join([dates[5], dates[3], dates[4]])
        # return redirect('/habitats/{}/{}'.format(from_date, to_date))  redirect to named url is also possible
        return render(request, 'homepage.html')
