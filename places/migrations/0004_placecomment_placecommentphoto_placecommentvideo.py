# Generated by Django 2.2.2 on 2019-07-14 13:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190608_0748'),
        ('places', '0003_place_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='امتیاز')),
                ('review', models.TextField(null=True, verbose_name='متن نظر')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place', verbose_name='مکان دیدنی')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Member', verbose_name='نویسندده')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceCommentVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='place_comments/videos/')),
                ('place_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='places.PlaceComment', verbose_name='نظر')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceCommentPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='place_comments/photos/', verbose_name='تصویر')),
                ('place_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.PlaceComment', verbose_name='نظر')),
            ],
        ),
    ]
