# Generated by Django 5.0.4 on 2024-05-03 12:37

import django_ckeditor_5.fields
import django_jalali.db.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritePDFCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
            ],
            options={
                'verbose_name': 'دوره پی\u200cدی\u200cافی مورد علاقه',
                'verbose_name_plural': 'دوره\u200cهای پی\u200cدی\u200cافی مورد علاقه',
                'db_table': 'account__favorite_pdf_course',
            },
        ),
        migrations.CreateModel(
            name='FavoriteVideoCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
            ],
            options={
                'verbose_name': 'دوره ویدئویی مورد علاقه',
                'verbose_name_plural': 'دوره\u200cهای ویدئویی مورد علاقه',
                'db_table': 'account__favorite_video_course',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_at', models.DateTimeField(auto_now_add=True, verbose_name='فالو شده در تاریخ')),
            ],
            options={
                'verbose_name': 'فالو',
                'verbose_name_plural': 'فالوها',
                'db_table': 'account__follow',
            },
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='آدرس ایمیل')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='آیا بلاک شده است؟')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
            ],
            options={
                'verbose_name': 'خبرنامه',
                'verbose_name_plural': 'خبرنامه\u200cها',
                'db_table': 'account__newsletter',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='یو\u200c\u200cیو\u200c\u200cآی\u200c\u200cدی')),
                ('title', models.CharField(max_length=100, verbose_name='تیتر')),
                ('message', django_ckeditor_5.fields.CKEditor5Field(verbose_name='پیام')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Account/Notification/image', verbose_name='تصویر')),
                ('image_link', models.URLField(blank=True, null=True, verbose_name='لینک تصویر')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('mode', models.CharField(choices=[('S', 'موفقیت (سبز)'), ('C', 'هشدار (نارنجی)'), ('D', 'خطر (قرمز)')], max_length=1, verbose_name='مود اعلان')),
                ('visibility', models.CharField(choices=[('GL', 'عمومی'), ('PV', 'شخصی')], max_length=2, verbose_name='وضعیت مشاهده')),
                ('type', models.CharField(choices=[('FO', 'فالو'), ('AN', 'اطلاعیه')], default='AN', max_length=2, verbose_name='نوع اعلان')),
                ('has_been_read', models.BooleanField(default=False, verbose_name='آیا خوانده شده؟')),
            ],
            options={
                'verbose_name': 'اعلانیه',
                'verbose_name_plural': 'اعلانات',
                'db_table': 'account__notification',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=75, null=True, verbose_name='نام کاربری')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='اسلاگ')),
                ('mobile_phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='رمز عبور')),
                ('sms_code', models.CharField(blank=True, max_length=4, null=True, verbose_name='کد تایید')),
                ('uuid', models.UUIDField(blank=True, null=True, verbose_name='یو یو آی دی')),
                ('otp_type', models.CharField(blank=True, choices=[('R', 'ثبت نام'), ('F', 'فراموشی رمز عبور'), ('D', 'حذف حساب کاربری'), ('UPH', 'به\u200c\u200cروز\u200c\u200cرسانی شماره تلفن')], max_length=3, null=True, verbose_name='نوع رمز یکبار مصرف')),
            ],
            options={
                'verbose_name': 'رمز یکبار مصرف',
                'verbose_name_plural': 'رمزهای یکبار مصرف',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=75, null=True, verbose_name='تیتر')),
                ('file', models.FileField(upload_to='Account/Posts/files/', verbose_name='فایل')),
                ('caption', models.TextField(blank=True, null=True, verbose_name='کپشن')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست\u200cها',
                'db_table': 'account__post',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund', models.PositiveBigIntegerField(default=0, verbose_name='سرمایه')),
                ('level', models.CharField(choices=[('T', 'تیتانیومی'), ('G', 'طلایی'), ('S', 'نقره\u200cای'), ('B', 'برنزی')], default='B', max_length=1, verbose_name='سطح')),
                ('difference', models.IntegerField(default=0, editable=False, verbose_name='میزان تفاوت')),
            ],
            options={
                'verbose_name': 'کیف پول',
                'verbose_name_plural': 'کیف\u200cهای پول',
                'db_table': 'account__wallet',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=75, unique=True, verbose_name='نام کاربری')),
                ('slug', models.SlugField(unique=True, verbose_name='اسلاگ')),
                ('mobile_phone', models.CharField(max_length=11, unique=True, verbose_name='شمارع تلفن')),
                ('authentication_token', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='یو یو آی دی')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='آدرس ایمیل')),
                ('full_name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('stars', models.PositiveIntegerField(default=0, verbose_name='تعداد ستاره')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='درباره من')),
                ('account_status', models.CharField(choices=[('PV', 'شخصی'), ('PU', 'عمومی')], default='PU', max_length=2, verbose_name='حالت اکانت')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Account/Users/profiles/', verbose_name='تصویر پروفایل')),
                ('is_staff', models.BooleanField(default=False, verbose_name='آیا کارمند است؟')),
                ('is_active', models.BooleanField(default=True, verbose_name='آیا فعال است؟')),
                ('date_joined', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ پیوستن')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
    ]
