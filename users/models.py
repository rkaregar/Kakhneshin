from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Member(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE, related_name='member')
    phone_number = models.CharField(max_length=12, default=0)

    def __str__(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def is_active(self):
        return self.user.is_active

    def save(self, *args, **kwargs):
        self.user.save()
        super().save(*args, **kwargs)


class ActivationCode(models.Model):
    member = models.ForeignKey(to=Member, related_name='activation_codes', on_delete=CASCADE)
    code = models.CharField(max_length=10)
