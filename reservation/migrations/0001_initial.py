# Generated by Django 2.2.2 on 2019-07-01 13:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habitats', '0009_roomtype_photo'),
        ('users', '0006_auto_20190608_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(verbose_name='تاریخ شروع')),
                ('to_date', models.DateField(verbose_name='تاریخ پایان')),
                ('is_active', models.BooleanField(default=False)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Member')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='habitats.RoomType')),
            ],
        ),
    ]
