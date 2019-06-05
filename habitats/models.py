from django.db import models
from users.models import Member


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='habitat template name')
    address = models.CharField(max_length=500, default='habitat template address')
    town = models.CharField(max_length=50, default='habitat template town')
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    # TODO: add new additional fields

    def __str__(self):
        return ','.join(map(str, [self.name, self.owner, self.address, self.town]))


class RoomType(models.Model):
    type_name = models.CharField(max_length=200, default='عادی')
    capacity_in_person = models.PositiveIntegerField(default=0)
    cost_per_night = models.PositiveIntegerField(default=0)
    has_breakfast = models.BooleanField(default=False)
    has_telephone = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    # TODO: add interior picture
    has_minibar = models.BooleanField(default=False)
    has_foreign_wc = models.BooleanField(default=False)
    has_bath_tub = models.BooleanField(default=False)
    has_shower = models.BooleanField(default=False)
    has_wc = models.BooleanField(default=False)
    details = models.CharField(max_length=10000, null=True)