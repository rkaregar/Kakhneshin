from accounts.models import Transaction
from django.forms import ModelForm


class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ('amount', )
