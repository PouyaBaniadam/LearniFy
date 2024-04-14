# Generated by Django 5.0.4 on 2024-04-14 19:13

import django.db.models.deletion
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
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('v', 'ویدئویی'), ('b', 'کتابی')], max_length=1, verbose_name='نوع')),
                ('course_id', models.PositiveSmallIntegerField(verbose_name='آیدی دوره')),
            ],
            options={
                'verbose_name': 'آیتم سبد خرید',
                'verbose_name_plural': 'آیتم\u200cهای سبد خرید',
                'db_table': 'cart__cart_item',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('PP', 'درکاه پرداخت'), ('CT', 'انتقال به کارت')], max_length=2, verbose_name='نحوه پرداخت')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('items', models.ManyToManyField(blank=True, related_name='cart_items', to='Cart.cartitem', verbose_name='آیتم\u200cهای سبد خرید')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبدهای خرید',
                'db_table': 'cart__cart',
            },
        ),
    ]
