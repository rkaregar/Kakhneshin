from accounts.models import Transaction
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Member


class Reservation(models.Model):
    from_date = models.DateField(verbose_name='تاریخ شروع')
    to_date = models.DateField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=False)

    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=1024, null=True, blank=True)

    member = models.ForeignKey(to=Member, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(to='habitats.RoomType', null=True, on_delete=models.SET_NULL)

    transaction = models.ForeignKey(to=Transaction, on_delete=models.CASCADE, verbose_name='تراکنش')
