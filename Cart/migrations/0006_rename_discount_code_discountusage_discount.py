# Generated by Django 5.0.4 on 2024-04-22 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0005_alter_discount_ends_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountusage',
            old_name='discount_code',
            new_name='discount',
        ),
    ]