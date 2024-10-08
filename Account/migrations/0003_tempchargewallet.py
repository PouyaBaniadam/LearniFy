# Generated by Django 5.0.4 on 2024-05-10 09:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempChargeWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_amount', models.PositiveSmallIntegerField(verbose_name='مقدار شارژ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'شارژ موقت کیف پول',
                'verbose_name_plural': 'شارژ\u200c\u200cهای موقت کیف پول',
                'db_table': 'account__temp_charge_wallet',
            },
        ),
    ]
