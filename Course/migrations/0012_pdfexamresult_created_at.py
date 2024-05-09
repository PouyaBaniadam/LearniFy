# Generated by Django 5.0.4 on 2024-05-08 15:22

import django.utils.timezone
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0011_alter_videocourse_coefficient_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfexamresult',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='ایجاد شده در تاریخ'),
            preserve_default=False,
        ),
    ]