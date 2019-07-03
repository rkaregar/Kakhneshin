from django.urls import path
from habitats.views.habitat_views import HabitatTinyDetailView, HomeView, HabitatDetailView, HabitatListView, \
    HabitatCreateView, HabitatDeleteView, HabitatUpdateView
from habitats.views.room_views import RoomTypeCreateView, RoomTypeDeleteView, RoomTypeUpdateView, RoomTypeDetailView, \
    RoomOutOfServiceView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HabitatListView.as_view(), name='all'),
    path('<int:habitat_pk>/', HabitatDetailView.as_view(), name='detail'),
    path('create/', HabitatCreateView.as_view(), name='habitat_create'),
    path('<int:habitat_pk>/delete/', HabitatDeleteView.as_view(), name='delete'),
    path('<int:habitat_pk>/update/', HabitatUpdateView.as_view(), name='habitat_update'),
    path('<int:habitat_pk>/detail/', HabitatTinyDetailView.as_view(), name='habitat_detail'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/delete', RoomTypeDeleteView.as_view(),
         name='delete_room_type'),
    path('<int:habitat_pk>/room_types/create', RoomTypeCreateView.as_view(), name='room_type_create'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/update', RoomTypeUpdateView.as_view(),
         name='room_type_update'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/detail', RoomTypeDetailView.as_view(),
         name='room_type_detail'),
    path('<int:habitat_pk>/room_types/<int:room_type_pk>/out_of_service', RoomOutOfServiceView.as_view(),
         name='room_out_of_service'),
]
