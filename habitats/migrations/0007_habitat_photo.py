# Generated by Django 2.2.2 on 2019-06-08 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0006_auto_20190608_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitat',
            name='photo',
            field=models.ImageField(null=True, upload_to='habitats'),
        ),
    ]
