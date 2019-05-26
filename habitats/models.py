from django.db import models


class Habitat(models.Model):
    name = models.CharField(max_length=200, default='habitat template name')
    address = models.CharField(max_length=500, default='habitat template address')
    town = models.CharField(max_length=50, default='habitat template town')
    cost = models.PositiveIntegerField(default=0)
