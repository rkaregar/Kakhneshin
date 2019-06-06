from django.urls import path, reverse_lazy
from habitats.views import HabitatCreateView, HabitatDeleteView, HabitatUpdateView, HabitatListView, HabitatDetailView, \
    HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HabitatListView.as_view(), name='all'),
    path('create/', HabitatCreateView.as_view(), name='create'),
    path('<int:habitat_pk>/', HabitatDetailView.as_view(), name='detail'),
    # path('<int:habitat_pk>/<slug:from_date>/<slug:to_date>/', HabitatDetailView.as_view(), name='detail'),
    path('<int:habitat_pk>/delete/', HabitatDeleteView.as_view(), name='delete'),
    path('<int:habitat_pk>/update/', HabitatUpdateView.as_view(), name='update'),
]
