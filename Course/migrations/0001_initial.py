# Generated by Django 5.0.4 on 2024-05-06 19:58

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import django_jalali.db.models
import mptt.fields
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
                ('icon', models.ImageField(blank=True, null=True, upload_to='Course/Category/icons/', verbose_name='آیکون')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='Course/Category/images', verbose_name='تصویر')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دسته بندی')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Course.category', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی\u200cها',
                'db_table': 'course__category',
            },
        ),
        migrations.CreateModel(
            name='PDFCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام دوره')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دوره')),
                ('what_we_will_learn', models.TextField(max_length=250, verbose_name='چی یاد میگیریم؟')),
                ('cover_image', models.ImageField(upload_to='Course/PDFCourse/cover_images', verbose_name='عکس کاور')),
                ('introduction_pdf', models.FileField(help_text='فقط PDF', upload_to='Course/PDFCourse/introduction_pdf', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='پی\u200cدی\u200cاف مقدمه')),
                ('holding_status', models.CharField(choices=[('NS', 'هنوز شروع نشده'), ('IP', 'در حال برگزاری'), ('F', 'به اتمام رسیده')], default='NS', max_length=2, verbose_name='وضعیت دوره')),
                ('coefficient_number', models.PositiveSmallIntegerField(default=1, help_text='یک عدد صحیح بین 1 تا 4', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='ضریب')),
                ('payment_type', models.CharField(choices=[('F', 'رایگان'), ('P', 'پولی')], default='F', max_length=1, verbose_name='نوع دوره')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت')),
                ('has_discount', models.BooleanField(default=False, verbose_name='تخفیف دارد؟')),
                ('discount_percentage', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('price_after_discount', models.PositiveBigIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروز\u200cرسانی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Course.category', verbose_name='دسته بندی')),
                ('participated_users', models.ManyToManyField(blank=True, editable=False, related_name='user_pdf_courses', to=settings.AUTH_USER_MODEL, verbose_name='کاربران ثبت نام شده')),
                ('prerequisites', models.ManyToManyField(blank=True, to='Course.pdfcourse', verbose_name='پیش نیاز دوره')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_pdf_courses', to=settings.AUTH_USER_MODEL, verbose_name='مدرس')),
            ],
            options={
                'verbose_name': 'دوره پی\u200cدی\u200cافی',
                'verbose_name_plural': 'دوره\u200cهای پی\u200cدی\u200cافی',
                'db_table': 'course__pdf_course',
            },
        ),
        migrations.CreateModel(
            name='PDFCourseComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='متن')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
                ('likes', models.ManyToManyField(blank=True, related_name='pdf_courses_comments_likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Course.pdfcoursecomment', verbose_name='والد')),
                ('pdf_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf_course_comments', to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pdf_course_comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت\u200cها',
                'db_table': 'course__pdf_course_comment',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='PDFCourseObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='تیتر')),
                ('download_file_name', models.CharField(help_text='فقط حروف انگلیسی و ارقام لاتین', max_length=50, verbose_name='نام فایل دانلودی')),
                ('note', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='یادداشت')),
                ('session', models.PositiveSmallIntegerField(default=1, verbose_name='قسمت')),
                ('pdf_file', models.FileField(help_text='فقط PDF', upload_to='Course/PDFCourse/tutorials', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='فایل پی\u200cدی\u200cاف')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='Course/PDFCourse/attachments', verbose_name='فایل ضمیمه')),
                ('can_be_sample', models.BooleanField(default=False, verbose_name='به عنوان نمونه تدریس انتخاب شود؟')),
                ('pages', models.PositiveIntegerField(default=0, verbose_name='تعداد صفحات پی\u200cدی\u200cاف')),
                ('pdf_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.pdfcourse', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'قسمت  دوره پی\u200cدی\u200cافی',
                'verbose_name_plural': 'قسمت\u200c\u200cهای دوره پی\u200cدی\u200cافی',
                'db_table': 'course__pdf_course_object',
            },
        ),
        migrations.CreateModel(
            name='PDFCourseObjectDownloadedBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایحاد')),
                ('pdf_course_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.pdfcourseobject', verbose_name='جزئیات پی\u200cدی\u200cاف')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دانلود شده توسط',
                'verbose_name_plural': 'دانلود شده توسط',
                'db_table': 'course__pdf_course_object_downloaded_by',
            },
        ),
        migrations.CreateModel(
            name='PDFCourseSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='شماره فصل')),
                ('name', models.CharField(max_length=75, verbose_name='اسم فصل')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.pdfcourse', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'فصل پی\u200cدی\u200cاف',
                'verbose_name_plural': 'فصل\u200cهای پی\u200cدی\u200cاف',
                'db_table': 'course__pdf_course_season',
            },
        ),
        migrations.AddField(
            model_name='pdfcourseobject',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfcourseseason', verbose_name='فصل'),
        ),
        migrations.CreateModel(
            name='PDFExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='نام آزمون')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('duration', models.DurationField(default=900, help_text='به ثانیه (پیش\u200c\u200cفرض: 15 دقیقه)', verbose_name='مدت زمان آزمون')),
                ('pdf_course_season', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Course.pdfcourseseason', verbose_name='فصل آزمون پی\u200c\u200cدی\u200c\u200cافی')),
            ],
            options={
                'verbose_name': 'آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'verbose_name_plural': 'آزمون\u200c\u200cهای پی\u200c\u200cدی\u200c\u200cافی',
                'db_table': 'course__pdf_exam',
            },
        ),
        migrations.CreateModel(
            name='PDFExamDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='صورت سوال')),
                ('question_number', models.PositiveSmallIntegerField(default=1, verbose_name='شماره سوال')),
                ('answer_1', models.CharField(max_length=200, verbose_name='گزینه 1')),
                ('answer_2', models.CharField(max_length=200, verbose_name='گزینه 2')),
                ('answer_3', models.CharField(max_length=200, verbose_name='گزینه 3')),
                ('answer_4', models.CharField(max_length=200, verbose_name='گزینه 4')),
                ('correct_answer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default=1, max_length=1, verbose_name='گزینه صحیح')),
                ('pdf_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfexam', verbose_name='آزمون پی\u200c\u200cدی\u200c\u200cافی')),
            ],
            options={
                'verbose_name': 'جواب آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'verbose_name_plural': 'جواب\u200c\u200cهای آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'db_table': 'course__pdf_exam_detail',
            },
        ),
        migrations.CreateModel(
            name='PDFExamFinalAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='صورت سوال')),
                ('selected_answer', models.CharField(max_length=200, verbose_name='گزینه انتخاب شده')),
                ('pdf_exam_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_answers', to='Course.pdfexamdetail', verbose_name='آزمون پی\u200c\u200cدی\u200c\u200cافی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ نهایی آزمون',
                'verbose_name_plural': 'پاسخ\u200c\u200cهای نهایی آزمون',
                'db_table': 'course__pdf_final_answer',
            },
        ),
        migrations.CreateModel(
            name='PDFExamTempAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='صورت سوال')),
                ('selected_answer', models.CharField(max_length=200, verbose_name='گزینه انتخاب شده')),
                ('pdf_exam_detail', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='temp_answers', to='Course.pdfexamdetail', verbose_name='آزمون پی\u200c\u200cدی\u200c\u200cافی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ موقت آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'verbose_name_plural': 'پاسخ\u200c\u200cهای موقت آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'db_table': 'course__pdf_temp_answer',
            },
        ),
        migrations.CreateModel(
            name='PDFExamTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='شروع شده در تاریخ')),
                ('ends_at', models.DateTimeField(verbose_name='پایان در تاریخ')),
                ('pdf_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.pdfexam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'زمان بندی آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'verbose_name_plural': 'زمان بندی\u200c\u200cهای آزمون پی\u200c\u200cدی\u200c\u200cافی',
                'db_table': 'course__pdf_exam_timer',
            },
        ),
        migrations.CreateModel(
            name='VideoCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام دوره')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='درباره دوره')),
                ('what_we_will_learn', models.TextField(max_length=250, verbose_name='چی یاد میگیریم؟')),
                ('cover_image', models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')),
                ('introduction_video', models.FileField(help_text='فرمت\u200c\u200cهای mp4 و mkv', upload_to='Course/VideoCourse/introduction_video', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv'])], verbose_name='فیلم مقدمه')),
                ('holding_status', models.CharField(choices=[('NS', 'هنوز شروع نشده'), ('IP', 'در حال برگزاری'), ('F', 'به اتمام رسیده')], default='NS', max_length=2, verbose_name='وضعیت دوره')),
                ('coefficient_number', models.PositiveSmallIntegerField(default=1, help_text='یک عدد صحیح بین 1 تا 4', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='ضریب')),
                ('payment_type', models.CharField(choices=[('F', 'رایگان'), ('P', 'پولی')], default='F', max_length=1, verbose_name='نوع دوره')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت')),
                ('has_discount', models.BooleanField(default=False, verbose_name='تخفیف دارد؟')),
                ('discount_percentage', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('price_after_discount', models.PositiveBigIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروز\u200cرسانی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Course.category', verbose_name='دسته بندی')),
                ('participated_users', models.ManyToManyField(blank=True, editable=False, related_name='user_video_courses', to=settings.AUTH_USER_MODEL, verbose_name='کاربران ثبت نام شده')),
                ('prerequisites', models.ManyToManyField(blank=True, to='Course.videocourse', verbose_name='پیش نیاز دوره')),
                ('teacher', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='teacher_video_courses', to=settings.AUTH_USER_MODEL, verbose_name='مدرس')),
            ],
            options={
                'verbose_name': 'دوره ویدئویی',
                'verbose_name_plural': 'دوره\u200cهای ویدئویی',
                'db_table': 'course__video_course',
            },
        ),
        migrations.CreateModel(
            name='BoughtCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveBigIntegerField(default=0, editable=False, verbose_name='قیمت خرید')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ایجاد شده در تاریخ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('pdf_course', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.pdfcourse', verbose_name='دوره پی\u200cدی\u200cافی')),
                ('video_course', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.videocourse', verbose_name='دوره ویدئویی')),
            ],
            options={
                'verbose_name': 'دوره خریداری شده',
                'verbose_name_plural': 'دوره\u200cهای خریداری شده',
                'db_table': 'course__bought_course',
            },
        ),
        migrations.CreateModel(
            name='VideoCourseComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='متن')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='به\u200cروز\u200cرسانی شده در تاریخ')),
                ('likes', models.ManyToManyField(blank=True, related_name='video_courses_comments_likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Course.videocoursecomment', verbose_name='والد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_video_course_comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('video_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_course_comments', to='Course.videocourse', verbose_name='دوره ویدئویی')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت\u200cها',
                'db_table': 'course__video_course_comment',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='VideoCourseObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='تیتر')),
                ('download_file_name', models.CharField(help_text='فقط حروف انگلیسی و ارقام لاتین', max_length=50, verbose_name='نام فایل دانلودی')),
                ('note', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='یادداشت')),
                ('session', models.PositiveSmallIntegerField(default=1, verbose_name='قسمت')),
                ('video_file', models.FileField(help_text='فرمت\u200c\u200cهای mp4 و mkv', upload_to='Course/VideoCourse/tutorials', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv'])], verbose_name='فایل ویدئو')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='Course/VideoCourse/attachments', verbose_name='فایل ضمیمه')),
                ('can_be_sample', models.BooleanField(default=False, verbose_name='به عنوان نمونه تدریس انتخاب شود؟')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='زمان فیلم')),
                ('video_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Course.videocourse', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'قسمت  دوره ویدئویی',
                'verbose_name_plural': 'قسمت\u200c\u200cهای دوره ویدئویی',
                'db_table': 'course__video_course_object',
            },
        ),
        migrations.CreateModel(
            name='VideoCourseObjectDownloadedBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایحاد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('video_course_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.videocourseobject', verbose_name='جزئیات ویدئو')),
            ],
            options={
                'verbose_name': 'دانلود شده توسط',
                'verbose_name_plural': 'دانلود شده توسط',
                'db_table': 'course__video_course_object_downloaded_by',
            },
        ),
        migrations.CreateModel(
            name='VideoCourseSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='شماره فصل')),
                ('name', models.CharField(max_length=75, verbose_name='اسم فصل')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.videocourse', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'فصل ویدئو',
                'verbose_name_plural': 'فصل\u200cهای ویدئو',
                'db_table': 'course__video_course_season',
            },
        ),
        migrations.AddField(
            model_name='videocourseobject',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.videocourseseason', verbose_name='فصل'),
        ),
        migrations.CreateModel(
            name='VideoExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='نام آزمون')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
                ('duration', models.DurationField(default=900, help_text='به ثانیه (پیش\u200c\u200cفرض: 15 دقیقه)', verbose_name='مدت زمان آزمون')),
                ('video_course_season', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Course.videocourseseason', verbose_name='فصل آزمون ویدئویی')),
            ],
            options={
                'verbose_name': 'آزمون ویدئویی',
                'verbose_name_plural': 'آزمون\u200c\u200cهای ویدئویی',
                'db_table': 'course__video_exam',
            },
        ),
        migrations.CreateModel(
            name='VideoExamDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveSmallIntegerField(default=1, verbose_name='شماره سوال')),
                ('question', models.CharField(max_length=200, verbose_name='صورت سوال')),
                ('answer_1', models.CharField(max_length=200, verbose_name='گزینه 1')),
                ('answer_2', models.CharField(max_length=200, verbose_name='گزینه 2')),
                ('answer_3', models.CharField(max_length=200, verbose_name='گزینه 3')),
                ('answer_4', models.CharField(max_length=200, verbose_name='گزینه 4')),
                ('correct_answer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default=1, max_length=1, verbose_name='گزینه صحیح')),
                ('video_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.videoexam', verbose_name='آزمون ویدئویی')),
            ],
            options={
                'verbose_name': 'جواب آزمون ویدئویی',
                'verbose_name_plural': 'جواب\u200c\u200cهای آزمون ویدئویی',
                'db_table': 'course__video_exam_detail',
            },
        ),
    ]
