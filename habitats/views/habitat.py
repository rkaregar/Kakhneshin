from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin

from habitats.forms import CreateHabitatForm
from habitats.models import Habitat


class HabitatCreateView(SuccessMessageMixin, CreateView):
    form_class = CreateHabitatForm
    template_name = 'habitats/create_habitat.html'
    success_url = '/habitats/create'
    success_message = 'اقامتگاه %s با موفقیت ثبت شد!'

    def form_valid(self, form):
        form.instance.owner = self.request.user.member
        return super(HabitatCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')


class HabitatUpdateView(SuccessMessageMixin, UpdateView):
    form_class = CreateHabitatForm
    template_name = 'habitats/update_habitat.html'
    success_url = '/habitats/update'
    success_message = 'اقامتگاه %s با موفقیت ویرایش شد!'

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        habitat_pk = self.get_habitat_pk()
        return Habitat.objects.get(pk=habitat_pk)

    def get_success_url(self):
        habitat_pk = self.get_habitat_pk()
        return '/habitats/%s/update' % habitat_pk

    def get_success_message(self, cleaned_data):
        print(cleaned_data.get('name'))
        return self.success_message % cleaned_data.get('name')


class HabitatDeleteView(SuccessMessageMixin, DeleteView):
    success_url = '/habitats/'
    success_message = 'اقامتگاه %s با موفقیت حذف شد!'

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        habitat_pk = self.get_habitat_pk()
        return Habitat.objects.get(pk=habitat_pk)

    def get_success_message(self, cleaned_data):
        print(cleaned_data.get('name'))
        return self.success_message % cleaned_data.get('name')


class HabitatListView(ListView):
    model = Habitat
