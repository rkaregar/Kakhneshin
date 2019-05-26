from django.urls import path, reverse_lazy
from habitats.views import HabitatCreateView, HabitatDeleteView, HabitatUpdateView, HabitatListView

urlpatterns = [
    path('', HabitatListView.as_view(), name='all'),
    path('create/', HabitatCreateView.as_view(), name='create'),
    path('<int:habitat_pk>/delete/', HabitatDeleteView.as_view(), name='delete'),
    path('<int:habitat_pk>/update/', HabitatUpdateView.as_view(), name='update'),
]
