from django.db import models
from users.models import Member


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='نام')
    address = models.CharField(max_length=500, default='', verbose_name='آدرس')
    town = models.CharField(max_length=50, default='', verbose_name='شهر')
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, verbose_name='صاحب اقامتگاه')

    # TODO: add new additional fields

    def __str__(self):
        return ','.join(map(str, [self.name, self.owner]))


class RoomType(models.Model):
    habitat = models.ForeignKey(Habitat, null=True, on_delete=models.CASCADE, verbose_name=' نام اقامتگاه')
    type_name = models.CharField(max_length=200, default='عادی', verbose_name='نام نوع اتاق')
    capacity_in_person = models.PositiveIntegerField(default=0, verbose_name='ظرفیت افراد')
    cost_per_night = models.PositiveIntegerField(default=0, verbose_name='هزینه‌ی هر شب')
    has_breakfast = models.BooleanField(default=False, verbose_name='صبحانه')
    has_telephone = models.BooleanField(default=False, verbose_name='تلفون')
    has_wifi = models.BooleanField(default=False, verbose_name='اینترنت بی‌سیم')
    # TODO: add interior picture
    has_minibar = models.BooleanField(default=False, verbose_name='مینی‌بار')
    has_foreign_wc = models.BooleanField(default=False, verbose_name='دست‌شویی‌فرنگی')
    has_bath_tub = models.BooleanField(default=False, verbose_name='وان حمام')
    has_shower = models.BooleanField(default=False, verbose_name='دوش حمام')
    has_wc = models.BooleanField(default=False, verbose_name='دست‌شویی')
    details = models.CharField(max_length=10000, null=True, verbose_name='توضیحات')

    def __str__(self):
        return self.type_name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, null=True, on_delete=models.CASCADE,
                                  verbose_name='نوع اتاق')  # TODO: cascade?
    number = models.CharField(max_length=10, null=True, verbose_name='شماره‌ی اتاق')
    details = models.CharField(max_length=10000, null=True, verbose_name='توضیحات')


class RoomOutOfService(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='اتاق مورد نظر')
    inclusive_since = models.DateTimeField(verbose_name='تاریخ شروع')
    inclusive_until = models.DateTimeField(verbose_name='تاریخ پایان')
    details = models.CharField(max_length=1000, null=True, verbose_name='توضیحات')
