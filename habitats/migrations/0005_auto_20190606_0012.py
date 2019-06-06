# Generated by Django 2.2.1 on 2019-06-05 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habitats', '0004_roomtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, null=True)),
                ('details', models.CharField(max_length=10000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='roomtype',
            name='habitat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitats.Habitat'),
        ),
        migrations.CreateModel(
            name='RoomOutOfService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inclusive_since', models.DateTimeField()),
                ('inclusive_until', models.DateTimeField()),
                ('details', models.CharField(max_length=1000, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitats.Room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitats.RoomType'),
        ),
    ]
