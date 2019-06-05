from django.db import models
from users.models import Member


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='habitat template name')
    address = models.CharField(max_length=500, default='habitat template address')
    town = models.CharField(max_length=50, default='habitat template town')
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)

    # TODO: add new additional fields

    def __str__(self):
        return ','.join(map(str, [self.name, self.cost, self.address, self.town]))
