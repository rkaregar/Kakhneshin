from accounts.models import Transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ('amount', )


class WithdrawalForm(TransactionForm):

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount > Transaction.get_balance_from_user(self.request.user):
            raise ValidationError('مبلغ بیش از موجودی حساب شماست.')
        return amount

    def save(self, commit=True):
        self.instance.from_user = self.request.user
        result = super().save(commit)
        if result is not None and commit:
            messages.add_message(self.request, messages.INFO, 'درخواست شما ثبت شد.')
        return result

