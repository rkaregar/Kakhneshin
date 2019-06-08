# Generated by Django 2.2.1 on 2019-06-08 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0005_auto_20190606_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitat',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='address',
            field=models.CharField(default='', max_length=500, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='name',
            field=models.CharField(default='', max_length=200, unique=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Member', verbose_name='صاحب اقامتگاه'),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='town',
            field=models.CharField(default='', max_length=50, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='room',
            name='details',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.CharField(max_length=10, null=True, verbose_name='شماره\u200cی اتاق'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitats.RoomType', verbose_name='نوع اتاق'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='details',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='inclusive_since',
            field=models.DateTimeField(verbose_name='تاریخ شروع'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='inclusive_until',
            field=models.DateTimeField(verbose_name='تاریخ پایان'),
        ),
        migrations.AlterField(
            model_name='roomoutofservice',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitats.Room', verbose_name='اتاق مورد نظر'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='capacity_in_person',
            field=models.PositiveIntegerField(default=0, verbose_name='ظرفیت افراد'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='cost_per_night',
            field=models.PositiveIntegerField(default=0, verbose_name='هزینه\u200cی هر شب'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='details',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='habitat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitats.Habitat', verbose_name=' نام اقامتگاه'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_bath_tub',
            field=models.BooleanField(default=False, verbose_name='وان حمام'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_breakfast',
            field=models.BooleanField(default=False, verbose_name='صبحانه'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_foreign_wc',
            field=models.BooleanField(default=False, verbose_name='دست\u200cشویی\u200cفرنگی'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_minibar',
            field=models.BooleanField(default=False, verbose_name='مینی\u200cبار'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_shower',
            field=models.BooleanField(default=False, verbose_name='دوش حمام'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_telephone',
            field=models.BooleanField(default=False, verbose_name='تلفون'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_wc',
            field=models.BooleanField(default=False, verbose_name='دست\u200cشویی'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='has_wifi',
            field=models.BooleanField(default=False, verbose_name='اینترنت بی\u200cسیم'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='type_name',
            field=models.CharField(default='عادی', max_length=200, verbose_name='نام نوع اتاق'),
        ),
    ]
