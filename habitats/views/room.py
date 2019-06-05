from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from habitats.forms import CreateRoomForm, CreateRoomTypeForm
from habitats.models import RoomType, Room


class RoomTypeCreateView(CreateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/create_room_type.html'
    success_url = 'create'


class RoomTypeUpdateView(UpdateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/update_room_type.html'
    success_url = 'update'

    def get_room_type_pk(self):
        # TODO: check that I am the owner of the room type or the admin
        room_type_pk = self.kwargs.get('room_type_pk', None)  # TODO: add it to urls.py
        return room_type_pk

    def get_object(self, queryset=None):
        room_type_pk = self.get_room_type_pk()
        return RoomType.objects.get(pk=room_type_pk)


class RoomTypeDeleteView(DeleteView):
    template_name = 'room_types/room_type_confirm_delete.html'

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


class RoomCreateView(CreateView):
    form_class = CreateRoomForm
    template_name = 'rooms/create_room.html'
    success_url = 'create'


class RoomUpdateView(UpdateView):
    form_class = CreateRoomForm
    template_name = 'rooms/update_room.html'
    success_url = 'update'

    def get_room_pk(self):
        # TODO: check that I am the owner of the room type or the admin
        room_pk = self.kwargs.get('room_pk', None)  # TODO: add it to urls.py
        return room_pk

    def get_object(self, queryset=None):
        room_pk = self.get_room_pk()
        return Room.objects.get(pk=room_pk)


class RoomDeleteView(DeleteView):
    template_name = 'rooms/room_confirm_delete.html'

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
