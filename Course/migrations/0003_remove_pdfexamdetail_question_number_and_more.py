# Generated by Django 5.0.4 on 2024-05-07 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0002_remove_pdfexamtimer_pdf_exam_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdfexamdetail',
            name='question_number',
        ),
        migrations.RemoveField(
            model_name='pdfexamtimer',
            name='pdf_exam_detail',
        ),
        migrations.AddField(
            model_name='pdfexamtimer',
            name='pdf_exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfexam'),
        ),
    ]
