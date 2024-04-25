# Generated by Django 5.0.4 on 2024-04-25 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0005_boughtcourse_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boughtcourse',
            name='cost',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='قیمت خرید'),
        ),
        migrations.AlterField(
            model_name='boughtcourse',
            name='pdf_course',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی'),
        ),
        migrations.AlterField(
            model_name='boughtcourse',
            name='video_course',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.videocourse', verbose_name='دوره ویدئویی'),
        ),
    ]
