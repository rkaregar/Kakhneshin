from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
    path('<int:habitat_pk>/', ReservationHabitatView.as_view(), name='habitat'),
]
