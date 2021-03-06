from typing import List, Iterable, Tuple

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from users.models import Member
from reservation.models import Reservation
from django.urls import reverse
from django.db.models import Q, Sum

from datetime import datetime, timedelta


class GeographicDivision(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(to="habitats.GeographicDivision", null=True, blank=True, on_delete=models.CASCADE)
    is_city = models.BooleanField()

    def __str__(self):
        return self.name

    @cached_property
    def hierarchy_name(self):
        name = ''
        division = self
        while division is not None:
            name += '{}، '.format(division.name)
            division = division.region
        return name[:-2]

    @cached_property
    def get_province(self):
        division = self
        while division.region is not None and division.region.region is not None:
            division = division.region
        return division

    @cached_property
    def get_fathers(self):
        division = self
        fathers = []
        while division.region is not None:
            fathers.append(division.region)
            division = division.region
        return fathers

    @classmethod
    def get_all_provinces(cls):
        provinces = []
        for division in cls.objects.all():
            if division.region is not None and division.region.region is None:
                provinces.append(division)
        return provinces

    @classmethod
    def get_childs(cls, divison_pk):
        return cls.objects.filter(region__id=divison_pk).all()


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='نام', unique=True)
    address = models.CharField(max_length=500, default='', verbose_name='آدرس')
    town = models.ForeignKey(GeographicDivision, verbose_name='شهر', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, verbose_name='صاحب اقامتگاه')
    confirm = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='habitats', null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if Habitat.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError('اقامتگاهی با این اسم وجود دارد. نام دیگری انتخاب کنید.')

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Habitat, self).save(*args, **kwargs)

    def get_reserve_ready_out(self, date):
        today = date
        tomorrow = timezone.now()+timezone.timedelta(days=1)
        reserved, ready, out = 0, 0, 0
        for room_type in self.roomtype_set.all():
            res, rea, ou = list(room_type.get_reserve_ready_out_count_list(today, tomorrow))[0]
            reserved += res
            ready += rea
            out += ou
        return reserved, ready, out

    def empty_rooms_count(self):
        return self.get_reserve_ready_out(timezone.now())[1]


class RoomType(models.Model):
    habitat = models.ForeignKey(Habitat, null=True, on_delete=models.CASCADE, verbose_name=' نام اقامتگاه')
    type_name = models.CharField(max_length=200, default='عادی', verbose_name='نام نوع اتاق')

    capacity_in_person = models.PositiveIntegerField(default=0, verbose_name='ظرفیت افراد')
    cost_per_night = models.PositiveIntegerField(default=0, verbose_name='هزینه‌ی هر شب')
    number_of_rooms_of_this_kind = models.PositiveIntegerField(default=0, verbose_name='تعداد اتاق‌های از این نوع')

    has_breakfast = models.BooleanField(default=False, verbose_name='صبحانه')
    has_telephone = models.BooleanField(default=False, verbose_name='تلفون')
    has_wifi = models.BooleanField(default=False, verbose_name='اینترنت بی‌سیم')
    has_minibar = models.BooleanField(default=False, verbose_name='مینی‌بار')
    has_foreign_wc = models.BooleanField(default=False, verbose_name='دست‌شویی‌فرنگی')
    has_bath_tub = models.BooleanField(default=False, verbose_name='وان حمام')
    has_shower = models.BooleanField(default=False, verbose_name='دوش حمام')
    has_wc = models.BooleanField(default=False, verbose_name='دست‌شویی')
    details = models.CharField(max_length=10000, null=True, blank=True, verbose_name='توضیحات')
    photo = models.ImageField(upload_to='room_types/', null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.type_name

    @property
    def owner(self):
        return self.habitat.owner

    def validate_unique(self, exclude=None):
        qs = RoomType.objects.filter(habitat=self.habitat)
        if qs.filter(type_name=self.type_name).exclude(id=self.id).exists():
            raise ValidationError('نام انواع اتاق در هر اقامتگاه باید یکتا باشد.')

    def has_empty_room(self, from_date, to_date):
        return self.has_empty_rooms(from_date, to_date, 1)

    def get_reserve_ready_out_count_list(self, from_date, to_date) -> Iterable[Tuple[int, int, int]]:
        out_list = self.get_out_of_service_rooms_count_list(from_date, to_date)
        reserve_list = self.get_reserved_rooms_count_list(from_date, to_date)
        for out, reserve in zip(out_list, reserve_list):
            yield reserve, self.number_of_rooms_of_this_kind - out - reserve, out

    def get_out_of_service_rooms_count_list(self, from_date, to_date):
        intersected_out_of_services = RoomOutOfService.objects.filter(
            Q(room=self) & ~(Q(exclusive_until__lte=from_date) | Q(inclusive_since__gte=to_date)))

        count_list = []
        for day in [from_date + timedelta(i) for i in range((to_date - from_date).days)]:
            num_of_out_of_service_rooms = \
                intersected_out_of_services.filter(Q(inclusive_since__lte=day) & Q(exclusive_until__gt=day)).aggregate(
                    rooms=Sum('number_of_affected_rooms'))['rooms'] or 0
            count_list.append(num_of_out_of_service_rooms)
        return count_list

    def get_reserved_rooms_count_list(self, from_date, to_date):
        intersected_reservations = Reservation.objects.filter(
            Q(room=self) & Q(is_active=True) & ~(Q(to_date__lte=from_date) | Q(from_date__gte=to_date)))

        count_list = []
        for day in [from_date + timedelta(i) for i in range((to_date - from_date).days)]:
            num_of_reserved_rooms = intersected_reservations.filter(
                Q(from_date__lte=day) & Q(to_date__gt=day)).count() or 0
            count_list.append(num_of_reserved_rooms)

        return count_list

    def has_empty_rooms(self, from_date, to_date, num_of_affected_rooms):

        intersected_out_of_services = RoomOutOfService.objects.filter(
            Q(room=self) & ~(Q(exclusive_until__lte=from_date) | Q(inclusive_since__gte=to_date)))
        intersected_reservations = Reservation.objects.filter(
            Q(room=self) & Q(is_active=True) & ~(Q(to_date__lte=from_date) | Q(from_date__gte=to_date)))

        for day in [from_date + timedelta(i) for i in range((to_date - from_date).days)]:
            num_of_out_of_service_rooms = \
                intersected_out_of_services.filter(Q(inclusive_since__lte=day) & Q(exclusive_until__gt=day)).aggregate(
                    rooms=Sum('number_of_affected_rooms'))['rooms'] or 0
            num_of_reserved_rooms = intersected_reservations.filter(
                Q(from_date__lte=day) & Q(to_date__gt=day)).count() or 0

            if num_of_out_of_service_rooms + num_of_reserved_rooms + \
                    int(num_of_affected_rooms) > self.number_of_rooms_of_this_kind:
                return False

        return True

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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.room.has_empty_rooms(self.inclusive_since, self.exclusive_until,
                                         self.number_of_affected_rooms):
            raise ValidationError('اضافه کردن این محدودیت امکان‌پذیر نمی‌باشد.')

        super(RoomOutOfService, self).save()
