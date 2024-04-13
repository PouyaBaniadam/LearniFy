# Generated by Django 5.0.4 on 2024-04-13 11:12

import Home.validators
import django.core.validators
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
            name='ExamSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیحات')),
                ('coefficient', models.SmallIntegerField(default=1, verbose_name='ضریب')),
            ],
            options={
                'verbose_name': 'بخش آزمون',
                'verbose_name_plural': 'بخش\u200cهای آزمون',
                'db_table': 'course__exam_section',
            },
        ),
        migrations.CreateModel(
            name='ExamUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیحات')),
                ('coefficient', models.SmallIntegerField(default=1, verbose_name='ضریب درس')),
            ],
            options={
                'verbose_name': 'درس آزمون',
                'verbose_name_plural': 'دروس آزمون',
                'db_table': 'course__exam_unit',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='Course/Category/icons/', verbose_name='آیکون')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='Course/Category/images', verbose_name='تصویر')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دسته بندی')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Course.category', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی\u200cها',
                'db_table': 'course__category',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام آزمون')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('questions_file', models.FileField(upload_to='Course/Exam/pdf', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='فایل سوالات آزمون')),
                ('is_downloading_question_files_allowed', models.BooleanField(default=True, verbose_name='آیا دانلود سوالات آزمون مجاز است؟')),
                ('question_file_name', models.CharField(help_text='فقط انگلیسی', max_length=100, unique=True, validators=[Home.validators.english_language_validator], verbose_name='نام فایل')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره آزمون')),
                ('cover_image', models.ImageField(upload_to='Course/Exam/cover_images', verbose_name='عکس کاور')),
                ('level', models.CharField(choices=[('E', 'ساده'), ('N', 'متوسط'), ('H', 'پیچیده')], default='N', max_length=1, verbose_name='میزان سختی')),
                ('type', models.CharField(choices=[('F', 'رایگان'), ('P', 'پولی')], default='F', max_length=1, verbose_name='نوع دوره')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')),
                ('has_discount', models.BooleanField(default=False, verbose_name='تخفیف دارد؟')),
                ('discount_percentage', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('price_after_discount', models.PositiveSmallIntegerField(default=0, verbose_name='قیمت بعد از تخفیف')),
                ('total_duration', models.DurationField(default=0, verbose_name='مدت آزمون')),
                ('is_entrance_allowed', models.BooleanField(default=True, verbose_name='آیا ورود به آزمون مجاز است؟')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروز\u200cرسانی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Course.category', verbose_name='دسته بندی')),
                ('designer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='طراح')),
                ('participated_users', models.ManyToManyField(blank=True, related_name='user_exams', to=settings.AUTH_USER_MODEL, verbose_name='کاربران ثبت نام شده')),
            ],
            options={
                'verbose_name': 'آزمون',
                'verbose_name_plural': 'آزمون\u200cها',
                'db_table': 'course__exam',
            },
        ),
        migrations.CreateModel(
            name='EnteredExamUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.exam', verbose_name='آزمون')),
            ],
            options={
                'verbose_name': 'کاربر شرکت کرده در آزمون',
                'verbose_name_plural': 'کاربران شرکت کرده در آزمون',
                'db_table': 'course__entered_exam_user',
            },
        ),
        migrations.CreateModel(
            name='DownloadedQuestionFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.exam', verbose_name='آزمون')),
            ],
            options={
                'verbose_name': 'فایل دانلود شده',
                'verbose_name_plural': 'فایل\u200cهای دانلود شده',
                'db_table': 'course__downloaded_question_file',
            },
        ),
        migrations.CreateModel(
            name='ExamAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveSmallIntegerField(verbose_name='شماره سوال')),
                ('choice_1', models.CharField(max_length=100, verbose_name='گزینه 1')),
                ('choice_2', models.CharField(max_length=100, verbose_name='گزینه 2')),
                ('choice_3', models.CharField(max_length=100, verbose_name='گزینه 3')),
                ('choice_4', models.CharField(max_length=100, verbose_name='گزینه 4')),
                ('true_answer', models.CharField(choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], max_length=1, verbose_name='گزینه صحیح')),
                ('true_answer_explanation', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیحات اضافه پاسخ صحیح')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.exam', verbose_name='آزمون')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.examsection', verbose_name='بخش')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.examunit', verbose_name='درس')),
            ],
            options={
                'verbose_name': 'پاسخ آزمون',
                'verbose_name_plural': 'پاسخ\u200cهای آزمون',
                'db_table': 'course__exam_answer',
            },
        ),
        migrations.CreateModel(
            name='UserFinalAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='شماره سوال')),
                ('selected_answer', models.CharField(blank=True, choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], max_length=10, null=True, verbose_name='گزینه انتخاب شده')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.exam', verbose_name='آزمون')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ نهایی کاربر',
                'verbose_name_plural': 'پاسخ\u200cهای نهایی کابران',
                'db_table': 'course__user_final_answer',
            },
        ),
        migrations.CreateModel(
            name='UserTempAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='شماره سوال')),
                ('selected_answer', models.CharField(blank=True, choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], max_length=10, null=True, verbose_name='گزینه انتخاب شده')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.exam', verbose_name='آزمون')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ موقت کاربر',
                'verbose_name_plural': 'پاسخ\u200cهای موقت کابران',
                'db_table': 'course__user_temp_answer',
            },
        ),
        migrations.CreateModel(
            name='VideoCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام دوره')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دوره')),
                ('what_we_will_learn', django_ckeditor_5.fields.CKEditor5Field(max_length=500, verbose_name='چی یاد میگیریم؟')),
                ('cover_image', models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')),
                ('introduction_video', models.FileField(upload_to='Course/VideoCourse/introduction_video', verbose_name='فیلم مقدمه')),
                ('status', models.CharField(choices=[('NS', 'هنوز شروع نشده'), ('IP', 'در حال برگزاری'), ('F', 'به اتمام رسیده')], default='NS', max_length=2, verbose_name='وضعیت دوره')),
                ('total_seasons', models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل\u200cها')),
                ('total_sessions', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='تعداد قسمت\u200cها')),
                ('total_duration', models.PositiveIntegerField(default=0, verbose_name='مدت دوره')),
                ('type', models.CharField(choices=[('F', 'رایگان'), ('P', 'پولی')], default='F', max_length=1, verbose_name='نوع دوره')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')),
                ('has_discount', models.BooleanField(default=False, verbose_name='تخفیف دارد؟')),
                ('discount_percentage', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('price_after_discount', models.PositiveSmallIntegerField(default=0, verbose_name='قیمت بعد از تخفیف')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروز\u200cرسانی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Course.category', verbose_name='دسته بندی')),
                ('participated_users', models.ManyToManyField(blank=True, related_name='user_video_courses', to=settings.AUTH_USER_MODEL, verbose_name='کاربران ثبت نام شده')),
                ('prerequisites', models.ManyToManyField(blank=True, to='Course.videocourse', verbose_name='پیش نیاز دوره')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_video_courses', to=settings.AUTH_USER_MODEL, verbose_name='مدرس')),
            ],
            options={
                'verbose_name': 'دوره ویدئویی',
                'verbose_name_plural': 'دوره\u200cهای ویدئویی',
                'db_table': 'course__video_course',
            },
        ),
        migrations.CreateModel(
            name='VideoSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='شماره فصل')),
                ('name', models.CharField(max_length=75, verbose_name='اسم فصل')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.videocourse', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'فصل ویدئو',
                'verbose_name_plural': 'فصل\u200cهای ویدئو',
                'db_table': 'course__video_season',
            },
        ),
        migrations.CreateModel(
            name='VideoCourseObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='تیتر')),
                ('note', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='یادداشت')),
                ('can_be_sample', models.BooleanField(default=False, verbose_name='به عنوان نمونه تدریس انتخاب شود؟')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='Course/VideoCourse/tutorials', verbose_name='فایل ویدئو')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='Course/VideoCourse/attachments', verbose_name='فایل ضمیمه')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='زمان فیلم')),
                ('video_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.videocourse', verbose_name='دوره')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.videoseason', verbose_name='فصل')),
            ],
            options={
                'verbose_name': 'جزئیات فیلم',
                'verbose_name_plural': 'جزئیات فیلم',
                'db_table': 'course__video_course_object',
            },
        ),
    ]
