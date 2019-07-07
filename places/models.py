from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from habitats.models import GeographicDivision
from users.models import Member


class Place(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='نام', unique=True)
    address = models.CharField(max_length=500, default='', verbose_name='آدرس')
    town = models.ForeignKey(GeographicDivision, verbose_name='شهر', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='places', null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if Place.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError('مکان دیدنی با این اسم وجود دارد. نام دیگری انتخاب کنید.')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Place, self).save(*args, **kwargs)

