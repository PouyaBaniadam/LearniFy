# Generated by Django 5.0.4 on 2024-04-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0002_alter_videocourse_price_after_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfcourse',
            name='price_after_discount',
            field=models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف'),
        ),
    ]