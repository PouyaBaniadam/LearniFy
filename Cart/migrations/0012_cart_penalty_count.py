# Generated by Django 5.0.4 on 2024-04-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0011_alter_boughtcourse_pdf_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='penalty_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='تعداد دفعات خطا'),
        ),
    ]
