# Generated by Django 5.0.4 on 2024-04-24 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0010_alter_cartitem_course_type'),
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boughtcourse',
            name='pdf_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی'),
        ),
        migrations.AlterField(
            model_name='boughtcourse',
            name='video_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.videocourse', verbose_name='دوره ویدئویی'),
        ),
    ]
