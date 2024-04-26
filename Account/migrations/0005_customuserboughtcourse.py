# Generated by Django 5.0.4 on 2024-04-26 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_alter_notification_visibility'),
        ('Course', '0009_remove_boughtcourse_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserBoughtCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('video_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.videocourse', verbose_name='دوره ویدئویی')),
            ],
        ),
    ]