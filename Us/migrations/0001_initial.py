# Generated by Django 5.0.4 on 2024-04-13 11:12

import django.db.models.deletion
import django_ckeditor_5.fields
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='نام')),
                ('short_description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='توضیح مختصر')),
                ('what_we_do', django_ckeditor_5.fields.CKEditor5Field(verbose_name='چی کار می\u200cکنیم')),
            ],
            options={
                'verbose_name': 'درباره',
                'verbose_name_plural': 'درباره ما',
                'db_table': 'us__about_us',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_1', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن اول')),
                ('phone_2', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن دوم')),
                ('telegram_url', models.URLField(blank=True, null=True, verbose_name='لینک تلگرام')),
                ('telegram_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون تلگرام')),
                ('telegram_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='شماره تلگرام')),
                ('whats_App_url', models.URLField(blank=True, null=True, verbose_name='لینک واتس\u200cاپ')),
                ('whats_App_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون واتس\u200cاپ')),
                ('whats_App_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='شماره واتس اپ')),
                ('linkedIn_url', models.URLField(blank=True, null=True, verbose_name='لینک لینکدین')),
                ('linkedIn_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون لینکدین')),
                ('pinterest_url', models.URLField(blank=True, null=True, verbose_name='لینک پینترست')),
                ('pinterest_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون پینترست')),
                ('instagram_url', models.URLField(blank=True, null=True, verbose_name='لینک اینستاگرام')),
                ('instagram_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون اینستاگرام')),
                ('twitter_url', models.URLField(blank=True, null=True, verbose_name='لینک توییتر')),
                ('twitter_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون توییتر')),
                ('facebook_url', models.URLField(blank=True, null=True, verbose_name='لینک فیس\u200cبوک')),
                ('facebook_icon', models.ImageField(blank=True, null=True, upload_to='Us/SocialMedia/icons', verbose_name='آیکون فیس\u200cبوک')),
            ],
            options={
                'verbose_name': 'شبکه اجتماعی',
                'verbose_name_plural': 'شبکه\u200cهای اجتماعی',
                'db_table': 'us__social_media',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='آدرس ایمیل')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام و نام خانوادگی')),
                ('can_be_shown', models.BooleanField(default=False, verbose_name='مجوز نشان داده شدن دارد؟')),
                ('message', models.TextField(max_length=500, verbose_name='پیام')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام\u200cها',
                'db_table': 'us__message',
            },
        ),
    ]
