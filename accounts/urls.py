from accounts.views import ChargeView, CallbackView, UpdateTransaction, WithdrawalsView, WithdrawalApprovalView
from django.urls import path

urlpatterns = [
    path('deposit/', ChargeView.as_view(), name='deposit'),
    path('callback/<str:token>/', CallbackView.as_view(), name='callback'),
    path('withdrawals/', WithdrawalsView.as_view(), name='withdrawals'),
    path('withdrawal_approval/', WithdrawalApprovalView.as_view(), name='withdrawal_approval'),
    path('transactions/<int:pk>/update/', UpdateTransaction.as_view(), name='update'),
]
