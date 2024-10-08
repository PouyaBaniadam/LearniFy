# Generated by Django 5.0.4 on 2024-05-10 05:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Financial', '0003_tempdiscountstorage_total_price_with_discount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TempDiscountStorage',
            new_name='TempDiscountUsage',
        ),
        migrations.AlterModelOptions(
            name='tempdiscountusage',
            options={'verbose_name': 'مورد استفاده موقت از کد تخفیف', 'verbose_name_plural': 'موارد استفاده موقت از کد تخفیف'},
        ),
        migrations.AlterModelTable(
            name='tempdiscountusage',
            table='financial__temp_discount_usage',
        ),
    ]
