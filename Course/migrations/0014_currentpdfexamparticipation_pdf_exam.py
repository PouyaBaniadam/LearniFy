# Generated by Django 5.0.4 on 2024-05-09 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0013_remove_videoexam_video_course_season_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentpdfexamparticipation',
            name='pdf_exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfexam', verbose_name='آزمون پی\u200c\u200cدی\u200c\u200cافی'),
            preserve_default=False,
        ),
    ]
