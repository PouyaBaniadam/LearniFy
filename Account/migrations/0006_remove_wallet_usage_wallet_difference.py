# Generated by Django 5.0.4 on 2024-04-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_wallet_usage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='usage',
        ),
        migrations.AddField(
            model_name='wallet',
            name='difference',
            field=models.IntegerField(default=0, verbose_name='میزان تفاوت'),
        ),
    ]