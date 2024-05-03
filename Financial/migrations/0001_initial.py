# Generated by Django 5.0.4 on 2024-05-03 12:37

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import django_jalali.db.models
import utils.useful_functions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_counter', models.PositiveSmallIntegerField(default=0, verbose_name='تعداد دفعات خطا')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبدهای خرید',
                'db_table': 'financial__cart',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_type', models.CharField(choices=[('VID', 'ویدئویی'), ('PDF', 'پی\u200cدی\u200cافی')], max_length=3, verbose_name='نوع دوره')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Financial.cart')),
                ('pdf_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی')),
                ('video_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.videocourse', verbose_name='دوره ویدئویی')),
            ],
            options={
                'verbose_name': 'آیتم سبد خرید',
                'verbose_name_plural': 'آیتم\u200cهای سبد خرید',
                'db_table': 'financial__cart_item',
            },
        ),
        migrations.CreateModel(
            name='DepositSlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.ImageField(upload_to='Financial/DepositSlips/receipts', verbose_name='تصویر رسید')),
                ('discount_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد تخفیف')),
                ('total_cost', models.PositiveBigIntegerField(default=0, editable=False, verbose_name='مبلغ قابل پرداخت')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('difference_cash', models.PositiveBigIntegerField(default=0, verbose_name='ما به تفاوت')),
                ('type', models.CharField(choices=[('BUY', 'خرید'), ('WAL', 'شارژ کیف پول')], max_length=3, verbose_name='نوع')),
                ('tracking_number', models.CharField(default=utils.useful_functions.generate_random_integers, max_length=10, verbose_name='شماره پیگیری')),
                ('is_valid', models.BooleanField(default=False, verbose_name='آیا رسید معتبر است؟')),
                ('is_fake', models.BooleanField(default=False, verbose_name='آیا رسید فیک است؟')),
                ('has_been_finished', models.BooleanField(default=False, editable=False, verbose_name='کارها انجام شده؟')),
                ('admin', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='ادمین')),
                ('cart', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='Financial.cart', verbose_name='سبد خرید')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فیش واریزی',
                'verbose_name_plural': 'رسیدهای خرید',
                'db_table': 'financial__deposit_slip',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=utils.useful_functions.generate_discount_code, max_length=10, unique=True, verbose_name='کد تخفیف')),
                ('percent', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)], verbose_name='درصد تخفیف')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='درباره تخفیف')),
                ('type', models.CharField(choices=[('PU', 'عمومی'), ('PV', 'شخصی')], max_length=2, verbose_name='نوع تخفیف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('duration', models.DurationField(help_text='به ثانیه', verbose_name='مدت تخفیف')),
                ('ends_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='تاریخ انقضا')),
                ('usage_limits', models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='محدودیت استفاده به نفر')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تخفیف',
                'verbose_name_plural': 'تخفیفات',
                'db_table': 'financial__discount',
            },
        ),
        migrations.CreateModel(
            name='DiscountUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ استفاده')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Financial.discount', verbose_name='تخفیف')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مورد استفاده کد تخفیف',
                'verbose_name_plural': 'موارد استفاده کد تخفیف',
                'db_table': 'financial__discount_usage',
            },
        ),
    ]
