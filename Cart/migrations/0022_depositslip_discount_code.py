# Generated by Django 5.0.4 on 2024-04-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0021_remove_depositslip_discount_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositslip',
            name='discount_code',
            field=models.CharField(default=1, max_length=10, verbose_name='کد تخفیف'),
            preserve_default=False,
        ),
    ]
