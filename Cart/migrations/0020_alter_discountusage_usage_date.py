# Generated by Django 5.0.4 on 2024-04-25 20:01

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0019_rename_discount_depositslip_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountusage',
            name='usage_date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ استفاده'),
        ),
    ]
