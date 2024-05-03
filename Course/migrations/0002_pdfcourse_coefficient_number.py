# Generated by Django 5.0.4 on 2024-05-03 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfcourse',
            name='coefficient_number',
            field=models.PositiveSmallIntegerField(default=1, help_text='یک عدد صحیح بین 1 تا 4', verbose_name='ضریب'),
        ),
    ]