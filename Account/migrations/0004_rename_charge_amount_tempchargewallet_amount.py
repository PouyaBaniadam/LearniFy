# Generated by Django 5.0.4 on 2024-05-10 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_tempchargewallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempchargewallet',
            old_name='charge_amount',
            new_name='amount',
        ),
    ]
