# Generated by Django 2.2.1 on 2019-05-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitat',
            name='address',
            field=models.CharField(default='habitat template address', max_length=500),
        ),
        migrations.AddField(
            model_name='habitat',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='habitat',
            name='name',
            field=models.CharField(default='habitat template name', max_length=200),
        ),
        migrations.AddField(
            model_name='habitat',
            name='town',
            field=models.CharField(default='habitat template town', max_length=50),
        ),
    ]
