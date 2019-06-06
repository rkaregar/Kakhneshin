from accounts.models import Transaction
from django.forms import ModelForm


class ChargeForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ('amount', )
