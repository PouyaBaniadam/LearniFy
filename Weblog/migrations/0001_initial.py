# Generated by Django 5.0.4 on 2024-04-26 17:10

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='News/Category/icons/', verbose_name='آیکون')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='News/Category/images', verbose_name='تصویر')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دسته بندی')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی\u200cها',
                'db_table': 'weblog__category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ\u200cها',
                'db_table': 'weblog__tags',
            },
        ),
        migrations.CreateModel(
            name='Weblog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='محتوا')),
                ('cover_image', models.ImageField(upload_to='News/News/cover_images', verbose_name='تصویر کاور')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروز\u200cرسانی')),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='weblogs', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Weblog.category', verbose_name='دسته بندی')),
                ('tags', models.ManyToManyField(blank=True, related_name='weblogs', to='Weblog.tag', verbose_name='تگ\u200cها')),
            ],
            options={
                'verbose_name': 'وبلاگ',
                'verbose_name_plural': 'وبلاگ\u200cها',
                'db_table': 'weblog__weblog',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='متن')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
                ('likes', models.ManyToManyField(blank=True, related_name='weblog_comments_likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Weblog.comment', verbose_name='والد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_weblog_comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('weblog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weblog_comments', to='Weblog.weblog', verbose_name='وبلاگ')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت\u200cها',
                'db_table': 'weblog__comment',
                'ordering': ('-created_at',),
            },
        ),
    ]
