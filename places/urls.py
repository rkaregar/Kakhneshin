from django.urls import path

from places.views import PlaceTinyDetailView, PlaceCreateView, PlaceDeleteView, PlaceUpdateView, PlaceListView, \
    PlaceSearchView

urlpatterns = [
    path('', PlaceListView.as_view(), name='all'),
    path('create/', PlaceCreateView.as_view(), name='place_create'),
    path('<int:place_pk>/delete/', PlaceDeleteView.as_view(), name='place_delete'),
    path('<int:place_pk>/update/', PlaceUpdateView.as_view(), name='place_update'),
    path('<int:place_pk>/detail/', PlaceTinyDetailView.as_view(), name='place_detail'),
    path('search/', PlaceSearchView.as_view(), name='place_search'),
]
