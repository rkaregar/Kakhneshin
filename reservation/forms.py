from django import forms
from django.conf import settings


class HabitatSearchForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    division = forms.IntegerField(required=True)
    persons = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(HabitatSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = 'پر کردن این فیلد اجباری است.'

    def clean_division(self):
        data = self.cleaned_data['division']
        if data == -1:
            self.add_error('division','شهر وارد شده در پایگاه داده موجود نیست.')
            return None
        return data


from datetime import timedelta

from accounts.models import Transaction
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from reservation.models import Reservation


class ReservationForm(ModelForm):

    def __init__(self, member, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = None
        self.member = member

    def clean(self):
        cleaned_data = super().clean()
        room_type = cleaned_data.get('room')
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if room_type and from_date and to_date:
            days = (to_date - from_date) / timedelta(days=1) + 1
            required_money = room_type.cost_per_night * days
            self.cost = required_money
            balance = Transaction.get_balance_from_user(self.member.user)
            if balance < required_money:
                raise ValidationError('باید حداقل {} در حساب خود داشته باشد. لطفا حساب خود را شارژ کنید.'.format(
                    required_money
                ))
        cleaned_data['member'] = self.member

    def save(self, commit=True):
        if commit:
            self.instance.transaction = Transaction.objects.create(
                from_user=self.member.user, to_user=None, amount=self.cost, verified=True
            )
            self.instance.transaction = Transaction.objects.create(
                from_user=self.member.user, to_user=self.instance.room.habitat.owner.user,
                amount=self.cost * (1 - settings.RESERVATION_FEE), verified=False
            )
        return super().save(commit)

    class Meta:
        model = Reservation
        fields = ('room', 'to_date', 'from_date')
