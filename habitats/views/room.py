from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from habitats.forms import CreateRoomForm, CreateRoomTypeForm
from habitats.models import RoomType, Room


class RoomTypeCreateView(SuccessMessageMixin, CreateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/create_room_type.html'
    success_url = 'create'
    success_message = 'نوع اتاق %s با موفقیت ثبت شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('type_name')


class RoomTypeUpdateView(SuccessMessageMixin, UpdateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/update_room_type.html'
    success_url = 'update'
    success_message = 'نوع اتاق %s با موفقیت ویرایش شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('type_name')

    def get_room_type_pk(self):
        # TODO: check that I am the owner of the room type or the admin
        room_type_pk = self.kwargs.get('room_type_pk', None)  # TODO: add it to urls.py
        return room_type_pk

    def get_object(self, queryset=None):
        room_type_pk = self.get_room_type_pk()
        return RoomType.objects.get(pk=room_type_pk)


class RoomTypeDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'room_types/room_type_confirm_delete.html'
    success_message = 'نوع اتاق %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('type_name')

    def get_room_type_pk(self):
        room_type_pk = self.kwargs.get('room_type_pk', None)
        return room_type_pk

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        room_type_pk = self.get_room_type_pk()
        return RoomType.objects.get(pk=room_type_pk)

    def get_success_url(self):
        return reverse_lazy('habitats:all_room_types', args=[self.get_habitat_pk()])


class RoomTypeListView(ListView):
    template_name = 'room_types/room_type_list.html'
    model = RoomType


class RoomCreateView(SuccessMessageMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'rooms/create_room.html'
    success_url = 'create'
    success_message = ' اتاق %s با موفقیت ثبت شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('number')


class RoomUpdateView(SuccessMessageMixin, UpdateView):
    form_class = CreateRoomForm
    template_name = 'rooms/update_room.html'
    success_url = 'update'
    success_message = ' اتاق %s با موفقیت ویرایش شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('number')

    def get_room_pk(self):
        # TODO: check that I am the owner of the room type or the admin
        room_pk = self.kwargs.get('room_pk', None)  # TODO: add it to urls.py
        return room_pk

    def get_object(self, queryset=None):
        room_pk = self.get_room_pk()
        return Room.objects.get(pk=room_pk)


class RoomDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'rooms/room_confirm_delete.html'
    success_message = ' اتاق %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('number')

    def get_room_pk(self):
        room_pk = self.kwargs.get('room_pk', None)
        return room_pk

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        room_pk = self.get_room_pk()
        return Room.objects.get(pk=room_pk)

    def get_success_url(self):
        return reverse_lazy('habitats:all_rooms', args=[self.get_habitat_pk()])


class RoomListView(ListView):
    template_name = 'rooms/room_list.html'
    model = Room
