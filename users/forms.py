from django.contrib.auth.forms import UserCreationForm
from users.models import Member, ActivationCode, User
from django.core.mail import send_mail
from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import random


class MemberCreationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email_validator = EmailValidator(message=_('لطفا ایمیل خود را درست وارد نمایید'))
    phone_validator = RegexValidator(regex=r'^\d{6,18}$', message=_('لطفا شماره تماس خود را درست وارد نمایید'))
    email = forms.CharField(validators=[email_validator])
    phone = forms.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def notify(self, subject, message):
        print(subject)
        print(message)
        send_mail(subject, message, from_email='asdproject97982@gmail.com', recipient_list=[self.cleaned_data['email']],
                  fail_silently=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.save()
        code = random.randint(1000, 9999)
        member = Member.objects.create(user=user)
        ActivationCode.objects.create(member=member, code=code)
        message = user.username + 'عزیز\nلطفا با استفاده از کد {}، حساب کاربری خود را تایید کنید.'.format(code)  # + str(code)
        self.notify('کد تایید سامانهٔ کاخ‌نشین', message)
        return member


class MemberActivationForm(forms.ModelForm):
    class Meta:
        model = ActivationCode
        fields = ('code',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_code(self):
        activation_code_object = get_object_or_404(ActivationCode, member=self.user)
        if activation_code_object.code != self.cleaned_data['code']:
            raise ValidationError('کد تایید وارد شده نادرست است')
        else:
            self.user.user.is_active = True
            self.user.user.save()
        return self.cleaned_data['code']

