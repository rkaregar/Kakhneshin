import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Manager

from utils.observer import non_recurse


class TransactionManager(Manager):

    def get_queryset(self):
        Transaction.notify_observers()
        return super().get_queryset()

class Transaction(models.Model):

    _observers = []

    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    modified = models.DateTimeField(auto_now=True, verbose_name='زمان تغییر')
    amount = models.PositiveIntegerField(verbose_name='مبلغ')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True,
                                  related_name='from_transactions')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='to_transactions')
    verified = models.BooleanField(verbose_name='انجام شده', default=False)
    token = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    objects = TransactionManager()

    @staticmethod
    def get_balance_from_user(user):
        deposited_amount = Transaction.objects.filter(
            to_user=user, verified=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawn_amount = Transaction.objects.filter(
            from_user=user, verified=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return deposited_amount - withdrawn_amount

    @staticmethod
    def get_system_balance():
        return Transaction.get_balance_from_user(None)


    @staticmethod
    def register_observer(observer):
        Transaction._observers.append(observer)


    @staticmethod
    def notify_observers():
        for observer in Transaction._observers:
            observer.update()
