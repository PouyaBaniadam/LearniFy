# Generated by Django 5.0.4 on 2024-05-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Financial', '0002_tempdiscountstorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempdiscountstorage',
            name='total_price_with_discount',
            field=models.PositiveBigIntegerField(default=0, verbose_name='قیمت نهایی'),
        ),
    ]