# Generated by Django 5.0.4 on 2024-05-08 12:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0010_alter_pdfexamresult_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videocourse',
            name='coefficient_number',
            field=models.PositiveSmallIntegerField(default=1, help_text='یک عدد صحیح بین 1 تا 4 (با توجه به میزان سختی)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='ضریب'),
        ),
    ]
