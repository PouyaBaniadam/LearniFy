# Generated by Django 5.0.4 on 2024-04-22 09:04

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_alter_discount_created_at_alter_discount_ends_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='ends_at',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ انقضا'),
        ),
    ]