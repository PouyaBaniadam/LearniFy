# Generated by Django 5.0.4 on 2024-04-24 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_boughtcourse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boughtcourse',
            name='user',
        ),
        migrations.AddField(
            model_name='boughtcourse',
            name='deposit_slip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Cart.depositslip', verbose_name='رسید خرید'),
            preserve_default=False,
        ),
    ]