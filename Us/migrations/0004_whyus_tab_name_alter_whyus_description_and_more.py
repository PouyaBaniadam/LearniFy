# Generated by Django 5.0.4 on 2024-04-28 08:14

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Us', '0003_whyus'),
    ]

    operations = [
        migrations.AddField(
            model_name='whyus',
            name='tab_name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='whyus',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='whyus',
            name='icon',
            field=models.ImageField(upload_to='Us/WhyUs/icons', verbose_name='آیکون'),
        ),
        migrations.AlterField(
            model_name='whyus',
            name='image',
            field=models.ImageField(upload_to='Us/WhyUs/images', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='whyus',
            name='title',
            field=models.CharField(max_length=20, verbose_name='تیتر'),
        ),
    ]