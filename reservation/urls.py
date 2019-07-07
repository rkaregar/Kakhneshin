from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
    path('reserve', ReservationCreateView.as_view(), name='reserve'),
    path('list', ReservationListView.as_view(), name='list'),
    path('change', ReservationUpdateView.as_view(), name='change'),
]
