# Generated by Django 5.0.4 on 2024-04-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0013_alter_cart_penalty_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='penalty_count',
        ),
        migrations.AddField(
            model_name='cart',
            name='penalty_counter',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='تعداد دفعات خطا'),
        ),
    ]