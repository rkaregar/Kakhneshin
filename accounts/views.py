from accounts.forms import TransactionForm
from accounts.models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


class ChargeView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')
    template_name = 'accounts/deposit.html'
    form_class = TransactionForm

    def form_valid(self, form):
        transaction = Transaction.objects.create(to_user=self.request.user, verified=False, amount=form.cleaned_data['amount'])
        return redirect('accounts:callback', token=transaction.token)


class CallbackView(TemplateView):
    template_name = 'accounts/callback.html'

    def get_context_data(self, token):
        transaction = get_object_or_404(Transaction, token=token)
        transaction.verified = True
        transaction.save()
        return {'success': True, 'error': None}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

