from django.core.exceptions import ValidationError
from django.db import models
from users.models import Member


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

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(RoomType, self).save(*args, **kwargs)


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, null=True, on_delete=models.CASCADE,
                                  verbose_name='نوع اتاق')  # TODO: cascade?
    number = models.CharField(max_length=10, null=True, verbose_name='شماره‌ی اتاق')
    details = models.CharField(max_length=10000, null=True, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return self.number

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(number=self.number)
        if qs.filter(room_type__habitat=self.room_type.habitat).exclude(id=self.id).exists():
            raise ValidationError('شماره‌ی اتاق‌ها در هر اقامتگاه باید یکتا باشد.')

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Room, self).save(*args, **kwargs)


class RoomOutOfService(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='اتاق مورد نظر')
    inclusive_since = models.DateTimeField(verbose_name='تاریخ شروع')
    inclusive_until = models.DateTimeField(verbose_name='تاریخ پایان')
    details = models.CharField(max_length=1000, null=True, blank=True, verbose_name='توضیحات')

    def __str__(self):
        raise NotImplementedError
