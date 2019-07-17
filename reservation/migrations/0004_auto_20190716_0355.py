# Generated by Django 2.2.2 on 2019-07-15 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_transaction_token'),
        ('reservation', '0003_merge_20190707_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='fee_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fee_reservations', to='accounts.Transaction', verbose_name='تراکنش'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='punish_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='punish_reservations', to='accounts.Transaction', verbose_name='تراکنش'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='return_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_reservations', to='accounts.Transaction', verbose_name='تراکنش'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='accounts.Transaction', verbose_name='تراکنش'),
        ),
    ]
