# Generated by Django 5.0.4 on 2024-04-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0023_alter_depositslip_difference_cash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositslip',
            name='discount_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='کد تخفیف'),
        ),
    ]