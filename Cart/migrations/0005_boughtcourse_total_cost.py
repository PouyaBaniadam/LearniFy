# Generated by Django 5.0.4 on 2024-04-24 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0004_remove_boughtcourse_user_boughtcourse_deposit_slip'),
    ]

    operations = [
        migrations.AddField(
            model_name='boughtcourse',
            name='total_cost',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='مبلغ کل'),
        ),
    ]