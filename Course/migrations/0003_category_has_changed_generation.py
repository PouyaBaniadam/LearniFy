# Generated by Django 5.0.4 on 2024-04-30 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0002_category_generation_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='has_changed_generation',
            field=models.BooleanField(default=False, verbose_name='آیا نسل تغییر کرده؟'),
        ),
    ]