from django.core.exceptions import ValidationError
from django.db import models
from users.models import Member
from django.urls import reverse
from django.db.models import Q

from datetime import datetime, timedelta, date


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='نام', unique=True)
    address = models.CharField(max_length=500, default='', verbose_name='آدرس')
    town = models.CharField(max_length=50, default='', verbose_name='شهر')
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, verbose_name='صاحب اقامتگاه')
    confirm = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='habitats', null=True, blank=True, verbose_name='تصویر')

    # TODO: add new additional fields

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if Habitat.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError('اقامتگاهی با این اسم وجود دارد. نام دیگری انتخاب کنید.')

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Habitat, self).save(*args, **kwargs)


class RoomType(models.Model):
    habitat = models.ForeignKey(Habitat, null=True, on_delete=models.CASCADE, verbose_name=' نام اقامتگاه')
    type_name = models.CharField(max_length=200, default='عادی', verbose_name='نام نوع اتاق')

    capacity_in_person = models.PositiveIntegerField(default=0, verbose_name='ظرفیت افراد')
    cost_per_night = models.PositiveIntegerField(default=0, verbose_name='هزینه‌ی هر شب')
    number_of_rooms_of_this_kind = models.PositiveIntegerField(default=0, verbose_name='تعداد اتاق‌های از این نوع')

    has_breakfast = models.BooleanField(default=False, verbose_name='صبحانه')
    has_telephone = models.BooleanField(default=False, verbose_name='تلفون')
    has_wifi = models.BooleanField(default=False, verbose_name='اینترنت بی‌سیم')
    # TODO: add interior picture
    has_minibar = models.BooleanField(default=False, verbose_name='مینی‌بار')
    has_foreign_wc = models.BooleanField(default=False, verbose_name='دست‌شویی‌فرنگی')
    has_bath_tub = models.BooleanField(default=False, verbose_name='وان حمام')
    has_shower = models.BooleanField(default=False, verbose_name='دوش حمام')
    has_wc = models.BooleanField(default=False, verbose_name='دست‌شویی')
    details = models.CharField(max_length=10000, null=True, blank=True, verbose_name='توضیحات')
    photo = models.ImageField(upload_to='room_types/', null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.type_name

    def validate_unique(self, exclude=None):
        qs = RoomType.objects.filter(habitat=self.habitat)
        if qs.filter(type_name=self.type_name).exclude(id=self.id).exists():
            raise ValidationError('نام انواع اتاق در هر اقامتگاه باید یکتا باشد.')

    def is_limitation_valid(self, from_date, to_date, num_of_affected_rooms):
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')

        intersected_out_of_services = RoomOutOfService.objects.filter(
            ~Q(exclusive_until__lte=from_date) | ~Q(inclusive_since__gte=to_date))

        for day in [from_date + timedelta(i) for i in range((to_date - from_date).days)]:
            print(day)

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(RoomType, self).save(*args, **kwargs)


class RoomOutOfService(models.Model):
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='اتاق مورد نظر')
    inclusive_since = models.DateField(verbose_name='تاریخ شروع')
    exclusive_until = models.DateField(verbose_name='تاریخ پایان')
    number_of_affected_rooms = models.PositiveIntegerField(default=1, verbose_name='تعداد اتاق‌ها')
    details = models.CharField(max_length=1000, null=True, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return 'اتاق {}، از {} تا {}، دلیل: {}'.format(self.room, self.inclusive_since, self.exclusive_until,
                                                       self.details)

    def get_absolute_url(self):
        return reverse('habitats:room_out_of_service',
                       kwargs={'habitat_pk': self.room.habitat_id, 'room_type_pk': self.room_id})
