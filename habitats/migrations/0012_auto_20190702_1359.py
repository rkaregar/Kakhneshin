# Generated by Django 2.2.2 on 2019-07-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0011_delete_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomoutofservice',
            name='inclusive_since',
            field=models.DateField(verbose_name='تاریخ شروع'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='inclusive_until',
            field=models.DateField(verbose_name='تاریخ پایان'),
        ),
    ]