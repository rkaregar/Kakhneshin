from accounts.models import Transaction
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

GENDERS = (('M', 'مرد'),
           ('F', 'زن'),
           ('O', 'سایر'),
           ('N', 'نمی‌خواهم اعلام کنم'))


class Member(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE, related_name='member')

    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    gender = models.CharField(choices=GENDERS, max_length=1, null=True)
    photo = models.ImageField(upload_to='members', null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True)
    is_habitat_owner = models.BooleanField(default=False, null=True, verbose_name='صاحب اقامت‌گاه؟')

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.last_name, self.user.username)

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def email(self):
        return self.user.email

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def balance(self):
        return Transaction.get_balance_from_user(self.user)

    def save(self, *args, **kwargs):
        self.user.save()
        super().save(*args, **kwargs)


class ActivationCode(models.Model):
    member = models.ForeignKey(to=Member, related_name='activation_codes', on_delete=CASCADE)
    code = models.CharField(max_length=10)
