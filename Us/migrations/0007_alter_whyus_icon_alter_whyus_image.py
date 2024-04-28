# Generated by Django 5.0.4 on 2024-04-28 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Us', '0006_alter_whyus_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whyus',
            name='icon',
            field=models.ImageField(help_text='64x64', upload_to='Us/WhyUs/icons', verbose_name='آیکون'),
        ),
        migrations.AlterField(
            model_name='whyus',
            name='image',
            field=models.ImageField(help_text='500x700', upload_to='Us/WhyUs/images', verbose_name='تصویر'),
        ),
    ]
