# Generated by Django 5.0.4 on 2024-04-25 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0018_depositslip_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depositslip',
            old_name='discount',
            new_name='discount_code',
        ),
    ]
