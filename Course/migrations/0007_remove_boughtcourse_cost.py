# Generated by Django 5.0.4 on 2024-04-26 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0006_alter_boughtcourse_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boughtcourse',
            name='cost',
        ),
    ]
