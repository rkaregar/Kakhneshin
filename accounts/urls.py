from accounts.views import ChargeView, CallbackView
from django.urls import path
urlpatterns = [
    path('deposit/', ChargeView.as_view(), name='deposit'),
    path('callback/<str:token>/', CallbackView.as_view(), name='callback'),
]
