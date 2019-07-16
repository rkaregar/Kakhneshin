from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReservationSearchView.as_view(), name='search'),
    path('<int:habitat_pk>/', ReservationHabitatView.as_view(), name='habitat'),
    path('<int:reservation_pk>/create_comment/', ReservationCommentView.as_view(), name='create_reservation_comment'),
    path('reserve', ReservationCreateView.as_view(), name='reserve'),
    path('cancel/<int:reservation_id>/', ReservationCancelView.as_view(), name='cancel'),
    path('list', ReservationListView.as_view(), name='list'),
]
