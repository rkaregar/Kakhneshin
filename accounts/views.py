from accounts.forms import TransactionForm, WithdrawalForm
from accounts.models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, ListView, UpdateView, CreateView


class ChargeView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')
    template_name = 'accounts/deposit.html'
    form_class = TransactionForm

    def form_valid(self, form):
        transaction = Transaction.objects.create(to_user=self.request.user, verified=False,
                                                 amount=form.cleaned_data['amount'])
        return redirect('accounts:portal', token=transaction.token)


class CallbackView(TemplateView):
    template_name = 'accounts/callback.html'

    def get_context_data(self, token):
        transaction = get_object_or_404(Transaction, token=token)
        transaction.verified = self.request.GET['status'] == 'OK'
        transaction.save()
        return {'success': True} if transaction.verified else {
            'success': transaction.verified,
            'error': self.request.GET['error']
        }



class PortalView(TemplateView):
    template_name = 'accounts/portal.html'

    def get_context_data(self, token):
        return {'token': token}


class WithdrawalsView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    template_name = 'accounts/withdrawals.html'
    form_class = WithdrawalForm
    success_url = reverse_lazy('accounts:withdrawals')

    def get_context_data(self, *, object_list=None, **kwargs):
        super_context = super().get_context_data(object_list=object_list, **kwargs)
        super_context['transactions'] = Transaction.objects.filter(
            from_user=self.request.user, verified=False, to_user=None
        )
        return super_context

    def get_form_class(self):
        class RequestForm(self.form_class):
            request = self.request

        return RequestForm


@method_decorator(staff_member_required, name='dispatch')
class WithdrawalApprovalView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('admin:login')
    model = Transaction
    template_name = 'accounts/withdrawal_approval.html'

    def get_queryset(self):
        return super().get_queryset().filter(verified=False, to_user=None)


@method_decorator(staff_member_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTransaction(UpdateView):
    success_url = reverse_lazy('accounts:withdrawal_approval')
    model = Transaction
    fields = ('verified',)
    template_name = 'accounts/withdrawal_approval.html'
