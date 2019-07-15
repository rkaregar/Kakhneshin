from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Member


class Reservation(models.Model):
    from_date = models.DateField(verbose_name='تاریخ شروع')
    to_date = models.DateField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=False)

    member = models.ForeignKey(to=Member, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(to='habitats.RoomType', null=True, on_delete=models.SET_NULL)

    # TODO: add the transaction field

    def __str__(self):
        return 'رزرو از تاریخ {} تا {}، توسط {} و اتاق {}'.format(self.from_date, self.to_date, self.member.name,
                                                                      self.room)


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
