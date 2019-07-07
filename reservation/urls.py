from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
    path('<int:habitat_pk>/', ReservationHabitatView.as_view(), name='habitat'),
    path('reserve', ReservationCreateView.as_view(), name='reserve'),
    path('list', ReservationListView.as_view(), name='list'),
    path('change', ReservationUpdateView.as_view(), name='change'),
]
