from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from habitats.models import GeographicDivision
from users.models import Member


class Place(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='نام', unique=True)
    address = models.CharField(max_length=500, default='', verbose_name='آدرس')
    town = models.ForeignKey(GeographicDivision, verbose_name='شهر', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='places', null=True, blank=True, verbose_name='تصویر')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name='سازندهٔ مکان')

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if Place.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError('مکان دیدنی با این اسم وجود دارد. نام دیگری انتخاب کنید.')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Place, self).save(*args, **kwargs)


class DistanceHabitatToPlace(models.Model):
    place = models.ForeignKey(to='places.Place', on_delete=models.CASCADE, verbose_name='مکان گردشگری')
    habitat = models.ForeignKey(to='habitats.Habitat', on_delete=models.CASCADE, verbose_name='اقامتگاه')
    distance = models.FloatField(verbose_name='فاصله (کیلومتر)')

    def __str__(self):
        return 'فاصله از {} تا {} برابر با {} کیلومتر'.format(self.habitat, self.place, self.distance)


class PlaceComment(models.Model):
    place = models.ForeignKey(to='places.Place', on_delete=models.CASCADE, verbose_name='مکان دیدنی')
    writer = models.ForeignKey(to='users.Member', on_delete=models.SET_NULL, null=True, verbose_name='نویسندده')

    rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 verbose_name='امتیاز')
    review = models.TextField(null=True, verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')

    def __str__(self):
        return 'نظر {} برای اقامتگاه {}: {}. امتیاز: {}'.format(self.writer, self.place, self.review, self.rating)


class PlaceCommentPhoto(models.Model):
    place_comment = models.ForeignKey(to='places.PlaceComment', on_delete=models.CASCADE, related_name='photos',
                                      verbose_name='نظر')
    photo = models.ImageField(upload_to='place_comments/photos/', verbose_name='تصویر')


class PlaceCommentVideo(models.Model):
    place_comment = models.ForeignKey(to='places.PlaceComment', on_delete=models.CASCADE, related_name='videos',
                                      verbose_name='نظر')
    video = models.FileField(upload_to='place_comments/videos/')
