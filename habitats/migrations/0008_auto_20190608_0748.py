# Generated by Django 2.2.2 on 2019-06-08 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0007_habitat_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitat',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='habitats', verbose_name='تصویر'),
        ),
    ]
