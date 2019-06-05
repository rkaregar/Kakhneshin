from django.urls import path, reverse_lazy
from habitats.views import HabitatCreateView, HabitatDeleteView, HabitatUpdateView, HabitatListView
from habitats.views.room import RoomTypeCreateView, RoomTypeDeleteView, RoomTypeUpdateView, RoomTypeListView, \
    RoomUpdateView, RoomDeleteView, RoomCreateView, RoomListView

urlpatterns = [
    path('', HabitatListView.as_view(), name='all'),
    path('create/', HabitatCreateView.as_view(), name='create'),
    path('<int:habitat_pk>/delete/', HabitatDeleteView.as_view(), name='delete'),
    path('<int:habitat_pk>/update/', HabitatUpdateView.as_view(), name='update'),
    path('<int:habitat_pk>/room_types/', RoomTypeListView.as_view(), name='all_room_types'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/delete', RoomTypeDeleteView.as_view(), name='delete_room_type'),
    path('<int:habitat_pk>/room_types/create', RoomTypeCreateView.as_view(), name='create_room_type'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/update', RoomTypeUpdateView.as_view(), name='update_room_type'),
    path('<int:habitat_pk>/rooms/<int:room_pk>/update', RoomUpdateView.as_view(), name='update_room'),
    path('<int:habitat_pk>/rooms/<int:room_pk>/delete', RoomDeleteView.as_view(), name='delete_room'),
    path('<int:habitat_pk>/rooms/create', RoomCreateView.as_view(), name='create_room'),
    path('<int:habitat_pk>/rooms/', RoomListView.as_view(), name='all_rooms'),
]

