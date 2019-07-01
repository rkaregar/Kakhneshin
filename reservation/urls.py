from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
]
