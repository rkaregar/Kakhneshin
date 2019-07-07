# Generated by Django 2.2.1 on 2019-07-07 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habitats', '0018_habitat_town'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, unique=True, verbose_name='نام')),
                ('address', models.CharField(default='', max_length=500, verbose_name='آدرس')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='places', verbose_name='تصویر')),
                ('town', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitats.GeographicDivision', verbose_name='شهر')),
            ],
        ),
    ]
