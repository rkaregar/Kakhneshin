from django.urls import path

from places.views import PlaceTinyDetailView, PlaceCreateView, PlaceDeleteView, PlaceUpdateView, PlaceListView

urlpatterns = [
    path('', PlaceListView.as_view(), name='all'),
    path('create/', PlaceCreateView.as_view(), name='place_create'),
    path('<int:place_pk>/delete/', PlaceDeleteView.as_view(), name='delete'),
    path('<int:place_pk>/update/', PlaceUpdateView.as_view(), name='place_update'),
    path('<int:place_pk>/detail/', PlaceTinyDetailView.as_view(), name='place_detail'),
]
