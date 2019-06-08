from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from habitats.forms import CreateRoomForm, CreateRoomTypeForm
from habitats.models import RoomType, Room, Habitat


class RoomTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/create_room_type.html'
    success_url = 'create'
    success_message = 'نوع اتاق %s با موفقیت ثبت شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('type_name')

    def set_habitat_pk(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)

    def get_initial(self):
        initial = super(RoomTypeCreateView, self).get_initial()
        self.set_habitat_pk()
        initial['habitat'] = self.habitat
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.set_habitat_pk()
        if self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان ایجاد نوع اتاق برای این اقامتگاه را ندارید.')
        return super(RoomTypeCreateView, self).dispatch(request, *args, **kwargs)


class RoomTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CreateRoomTypeForm
    template_name = 'room_types/update_room_type.html'
    success_url = 'update'
    success_message = 'نوع اتاق %s با موفقیت ویرایش شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('type_name')

    def get_object(self, queryset=None):
        return self.room_type

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_type_pk = self.kwargs.get('room_type_pk', None)
        self.room_type = get_object_or_404(RoomType, pk=room_type_pk)

    def get_initial(self):
        initial = super(RoomTypeUpdateView, self).get_initial()
        initial['habitat'] = self.habitat
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان ویرایش نوع اتاق برای این اقامتگاه را ندارید.')
        return super(RoomTypeUpdateView, self).dispatch(request, *args, **kwargs)


class RoomTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
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

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_type_pk = self.kwargs.get('room_type_pk', None)
        self.room_type = get_object_or_404(RoomType, pk=room_type_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان حذف نوع اتاق برای این اقامتگاه را ندارید.')
        return super(RoomTypeDeleteView, self).dispatch(request, *args, **kwargs)


class RoomTypeListView(LoginRequiredMixin, ListView):
    template_name = 'room_types/room_type_list.html'
    model = RoomType

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان مشاهده‌ی انواع اتاق برای این اقامتگاه را ندارید.')
        return super(RoomTypeListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(RoomTypeListView, self).get_queryset()
        return qs.filter(habitat=self.habitat)

    def get_context_data(self, **kwargs):
        context = super(RoomTypeListView, self).get_context_data(**kwargs)
        context['habitat_pk'] = self.habitat_pk
        return context


class RoomCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'rooms/create_room.html'
    success_url = 'create'
    success_message = ' اتاق %s با موفقیت ثبت شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('number')


class RoomUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_pk = self.kwargs.get('room_pk', None)
        self.room = get_object_or_404(Room, pk=room_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان مشاهده‌ی اتاق برای این اقامتگاه را ندارید.')
        return super(RoomUpdateView, self).dispatch(request, *args, **kwargs)


class RoomTypeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'room_types/room_type_detail.html'

    def get_room_type_pk(self):
        room_type_pk = self.kwargs.get('room_type_pk', None)
        return room_type_pk

    def get_habitat_pk(self):
        habitat_pk = self.kwargs.get('habitat_pk', None)
        return habitat_pk

    def get_object(self, queryset=None):
        room_type_pk = self.get_room_type_pk()
        return RoomType.objects.get(pk=room_type_pk)

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_type_pk = self.kwargs.get('room_type_pk', None)
        self.room_type = get_object_or_404(RoomType, pk=room_type_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان مشاهده‌ی نوع اتاق برای این اقامتگاه را ندارید.')
        return super(RoomTypeDetailView, self).dispatch(request, *args, **kwargs)


class RoomDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
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

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_pk = self.kwargs.get('room_pk', None)
        self.room = get_object_or_404(Room, pk=room_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان حذف اتاق برای این اقامتگاه را ندارید.')
        return super(RoomDeleteView, self).dispatch(request, *args, **kwargs)


class RoomListView(LoginRequiredMixin, ListView):
    template_name = 'rooms/room_list.html'
    model = Room

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان مشاهده‌ی اتاق‌های این اقامتگاه را ندارید.')
        return super(RoomListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(RoomListView, self).get_queryset()
        return qs.filter(room_type__habitat=self.habitat)

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['habitat_pk'] = self.habitat_pk
        return context


class RoomDetailView(LoginRequiredMixin, DetailView):
    template_name = 'rooms/room_detail.html'

    def get_room_pk(self):
        # TODO: check that I am the owner of the room type or the admin
        room_pk = self.kwargs.get('room_pk', None)  # TODO: add it to urls.py
        return room_pk

    def get_object(self, queryset=None):
        room_pk = self.get_room_pk()
        return Room.objects.get(pk=room_pk)

    def set_objects(self):
        self.habitat_pk = self.kwargs.get('habitat_pk', None)
        self.habitat = get_object_or_404(Habitat, pk=self.habitat_pk)
        room_pk = self.kwargs.get('room_pk', None)
        self.room = get_object_or_404(Room, pk=room_pk)

    def dispatch(self, request, *args, **kwargs):
        self.set_objects()
        if self.room.room_type.habitat != self.habitat or self.habitat.owner != self.request.user.member:
            raise PermissionDenied('شما امکان مشاهده‌ی جزییات اتاق برای این اقامتگاه را ندارید.')
        return super(RoomDetailView, self).dispatch(request, *args, **kwargs)
