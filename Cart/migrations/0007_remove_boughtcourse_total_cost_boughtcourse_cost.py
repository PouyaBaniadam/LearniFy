# Generated by Django 5.0.4 on 2024-04-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0006_remove_boughtcourse_deposit_slip_boughtcourse_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boughtcourse',
            name='total_cost',
        ),
        migrations.AddField(
            model_name='boughtcourse',
            name='cost',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='مبلغ'),
        ),
    ]