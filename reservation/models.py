from datetime import datetime, timedelta, date

from django.conf import settings

from accounts.models import Transaction
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Member
from utils.observer import non_recurse


class Reservation(models.Model):
    from_date = models.DateField(verbose_name='تاریخ شروع')
    to_date = models.DateField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=False)

    member = models.ForeignKey(to=Member, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(to='habitats.RoomType', null=True, on_delete=models.SET_NULL)

    transaction = models.ForeignKey(
        to=Transaction, on_delete=models.CASCADE, verbose_name='تراکنش',
        related_name='reservations'
    )
    fee_transaction = models.ForeignKey(
        to=Transaction, on_delete=models.CASCADE, verbose_name='تراکنش', null=True,
        related_name='fee_reservations'
    )
    punish_transaction = models.ForeignKey(
        to=Transaction, on_delete=models.CASCADE, verbose_name='تراکنش', null=True,
        related_name='punish_reservations'
    )
    return_transaction = models.ForeignKey(
        to=Transaction, on_delete=models.CASCADE, verbose_name='تراکنش', null=True,
        related_name='return_reservations'
    )

    @property
    def cost(self):
        return ((self.to_date - self.from_date) / timedelta(days=1)) * self.room.cost_per_night

    @property
    def can_cancel(self):
        return self.is_active and date.today() < self.from_date

    def cancel(self):
        if not self.can_cancel:
            return False
        cancellation_fee = 0
        today = date.today()
        if self.from_date - timedelta(days=10) < today:
            left_days = (self.from_date - today) / timedelta(days=1)
            cancellation_fee = settings.CANCELLATION_FEE * (settings.PUNISHED_CANCELLATION_DAYS - left_days)
        self.is_active = False
        cancellation_punish_amount = cancellation_fee * self.cost
        self.return_transaction = Transaction.objects.create(
            from_user=None, to_user=self.member.user, verified=True, amount=self.cost
        )
        self.punish_transaction = Transaction.objects.create(
            from_user=self.member.user, to_user=self.room.owner.user, verified=True, amount=cancellation_punish_amount
        )
        self.save()
        return True

    @staticmethod
    @non_recurse
    def update():
        today = date.today()
        Transaction.objects.filter(
            fee_reservations__from_date__lte=today,
            fee_reservations__is_active=True,
            verified=False
        ).update(verified=True)

    def __str__(self):
        return 'رزرو اتاق {} در اقامتگاه {}، از تاریخ {} تا {} با هزینهٔ {}'.format(self.room, self.room.habitat,
                                                                                    self.from_date, self.to_date,
                                                                                    self.cost)


Transaction.register_observer(Reservation)


class ReservationComment(models.Model):
    reservation = models.OneToOneField(to='reservation.Reservation', on_delete=models.CASCADE, related_name='comment',
                                       verbose_name='رزرو')

    rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 verbose_name='امتیاز')
    review = models.TextField(null=True, verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')

    def __str__(self):
        return 'نظر {} برای اقامتگاه {}: {}. امتیاز: {}'.format(self.reservation.member.name,
                                                                self.reservation.room.habitat, self.review, self.rating)


class ReservationCommentPhoto(models.Model):
    reservation_comment = models.ForeignKey(to='reservation.ReservationComment', on_delete=models.CASCADE,
                                            related_name='photos', verbose_name='نظر')
    photo = models.ImageField(upload_to='reservation_comments/photos/', verbose_name='تصویر')


class ReservationCommentVideo(models.Model):
    reservation_comment = models.ForeignKey(to='reservation.ReservationComment', on_delete=models.CASCADE,
                                            related_name='videos', verbose_name='نظر')
    video = models.FileField(upload_to='reservation_comments/videos/')
