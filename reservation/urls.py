from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
    path('<int:habitat_pk>/', ReservationHabitatView.as_view(), name='habitat'),
    path('<int:reservation_pk>/create_comment/', ReservationCommentView.as_view(), name='create_reservation_comment'),
]
