# Generated by Django 2.2.2 on 2019-07-01 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0009_roomtype_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='number_of_rooms_of_this_kind',
            field=models.PositiveIntegerField(default=0, verbose_name='تعداد اتاق\u200cهای از این نوع'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitats.RoomType', verbose_name='اتاق مورد نظر'),
        ),
    ]
