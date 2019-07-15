# Generated by Django 2.2.2 on 2019-07-06 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_transaction_token'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='transaction',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Transaction', verbose_name='تراکنش'),
            preserve_default=False,
        ),
    ]