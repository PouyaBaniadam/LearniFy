# Generated by Django 5.0.4 on 2024-05-08 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0009_pdfexamresult_none_answers_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfexamresult',
            name='percentage',
            field=models.FloatField(verbose_name='درصد'),
        ),
    ]
