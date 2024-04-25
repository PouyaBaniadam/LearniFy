import fitz
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from moviepy.editor import VideoFileClip


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True,
                               verbose_name='والد')

    icon = models.ImageField(upload_to='Course/Category/icons/', verbose_name='آیکون', blank=True, null=True)

    cover_image = models.ImageField(upload_to='Course/Category/images', verbose_name='تصویر', blank=True, null=True)

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'course__category'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'


class VideoCourse(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    HOLDING_STATUS_CHOICES = (
        ('NS', 'هنوز شروع نشده'),
        ('IP', 'در حال برگزاری'),
        ('F', 'به اتمام رسیده'),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='نام دوره')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دوره')

    what_we_will_learn = CKEditor5Field(config_name="extends", max_length=500, verbose_name='چی یاد میگیریم؟')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='مدرس',
                                related_name='teacher_video_courses')

    cover_image = models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')

    introduction_video = models.FileField(upload_to='Course/VideoCourse/introduction_video', verbose_name='فیلم مقدمه')

    holding_status = models.CharField(max_length=2, choices=HOLDING_STATUS_CHOICES, verbose_name='وضعیت دوره',
                                      default='NS')

    total_seasons = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل‌ها')

    total_sessions = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد قسمت‌ها')

    total_duration = models.PositiveIntegerField(default=0, verbose_name='مدت دوره')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_video_courses')

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.payment_type == "F":
            self.price = self.price_after_discount = self.discount_percentage = self.has_discount = 0

        if self.has_discount:
            self.price_after_discount = self.price - (self.price * (self.discount_percentage / 100))

        else:
            self.price_after_discount = self.price

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__video_course'
        verbose_name = 'دوره ویدئویی'
        verbose_name_plural = 'دوره‌های ویدئویی'


class VideoCourseComment(models.Model):
    video_course = models.ForeignKey(to=VideoCourse, on_delete=models.CASCADE, verbose_name="دوره ویدئویی",
                                     related_name='video_course_comments')

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر",
                             related_name="user_video_course_comments")

    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, verbose_name="والد", blank=True, null=True,
                               related_name="replies")

    text = models.TextField(max_length=1000, verbose_name="متن")

    likes = models.ManyToManyField(to="Account.CustomUser", verbose_name="لایک‌ها",
                                   related_name="video_courses_comments_likes", blank=True)

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    updated_at = jDateTimeField(auto_now=True, verbose_name='به‌روز‌رسانی شده در تاریخ')

    def __str__(self):
        return f"{self.user.username} - {self.video_course.name}"

    class Meta:
        db_table = 'course__video_course_comment'
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
        ordering = ('-created_at',)


class VideoCourseSeason(models.Model):
    number = models.PositiveSmallIntegerField(default=1, verbose_name="شماره فصل")

    name = models.CharField(max_length=75, verbose_name="اسم فصل")

    course = models.ForeignKey(to=VideoCourse, on_delete=models.CASCADE, verbose_name="دوره")

    def __str__(self):
        return f"{self.course.name} - {self.name} - {self.number}"

    class Meta:
        db_table = 'course__video_course_season'
        verbose_name = 'فصل ویدئو'
        verbose_name_plural = 'فصل‌های ویدئو'


class VideoCourseObject(models.Model):
    video_course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE, verbose_name="دوره", blank=True,
                                     null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=VideoCourseSeason, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name="فصل")

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    video_file = models.FileField(upload_to="Course/VideoCourse/tutorials", verbose_name="فایل ویدئو")

    attachment = models.FileField(upload_to="Course/VideoCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    duration = models.PositiveIntegerField(default=0, verbose_name="زمان فیلم")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            # Load the video file
            video_path = self.video_file.path
            clip = VideoFileClip(video_path)
            # Get the duration in seconds and save it
            self.duration = int(clip.duration)
            clip.close()
            # Update the model with the duration
            super().save(*args, **kwargs)
        except Exception as e:
            # Handle any exceptions, such as if the file is not found or is not a valid video file
            print(f"An error occurred while getting the duration of the video file: {e}")

    class Meta:
        db_table = 'course__video_course_object'
        verbose_name = 'جزئیات فیلم'
        verbose_name_plural = 'جزئیات فیلم'


class PDFCourse(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    HOLDING_STATUS_CHOICES = (
        ('NS', 'هنوز شروع نشده'),
        ('IP', 'در حال برگزاری'),
        ('F', 'به اتمام رسیده'),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='نام دوره')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دوره')

    what_we_will_learn = CKEditor5Field(config_name="extends", max_length=500, verbose_name='چی یاد میگیریم؟')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='مدرس',
                                related_name='teacher_pdf_courses')

    cover_image = models.ImageField(upload_to='Course/PDFCourse/cover_images', verbose_name='عکس کاور')

    introduction_pdf = models.FileField(upload_to='Course/PDFCourse/introduction_pdf', verbose_name='پی‌دی‌اف مقدمه')

    holding_status = models.CharField(max_length=2, choices=HOLDING_STATUS_CHOICES, verbose_name='وضعیت دوره',
                                      default='NS')

    total_seasons = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل‌ها')

    total_sessions = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد قسمت‌ها')

    total_pages = models.PositiveIntegerField(default=0, verbose_name='تعداد صفحات دوره')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_pdf_courses')

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.payment_type == "F":
            self.price = self.price_after_discount = self.discount_percentage = self.has_discount = 0

        if self.has_discount:
            self.price_after_discount = self.price - (self.price * (self.discount_percentage / 100))
        else:
            self.price_after_discount = self.price

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__pdf_course'
        verbose_name = 'دوره پی‌دی‌افی'
        verbose_name_plural = 'دوره‌های پی‌دی‌افی'


class PDFCourseComment(models.Model):
    pdf_course = models.ForeignKey(to=PDFCourse, on_delete=models.CASCADE, verbose_name="دوره پی‌دی‌افی",
                                   related_name='pdf_course_comments')

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر",
                             related_name="user_pdf_course_comments")

    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, verbose_name="والد", blank=True, null=True,
                               related_name="replies")

    text = models.TextField(max_length=1000, verbose_name="متن")

    likes = models.ManyToManyField(to="Account.CustomUser", verbose_name="لایک‌ها",
                                   related_name="pdf_courses_comments_likes", blank=True)

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    updated_at = jDateTimeField(auto_now=True, verbose_name='به‌روز‌رسانی شده در تاریخ')

    def __str__(self):
        return f"{self.user.username} - {self.pdf_course.name}"

    class Meta:
        db_table = 'course__pdf_course_comment'
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
        ordering = ('-created_at',)


class PDFCourseSeason(models.Model):
    number = models.PositiveSmallIntegerField(default=1, verbose_name="شماره فصل")

    name = models.CharField(max_length=75, verbose_name="اسم فصل")

    course = models.ForeignKey(to=PDFCourse, on_delete=models.CASCADE, verbose_name="دوره")

    def __str__(self):
        return f"{self.course.name} - {self.name} - {self.number}"

    class Meta:
        db_table = 'course__pdf_course_season'
        verbose_name = 'فصل پی‌دی‌اف'
        verbose_name_plural = 'فصل‌های پی‌دی‌اف'


class PDFCourseObject(models.Model):
    pdf_course = models.ForeignKey(PDFCourse, on_delete=models.CASCADE, verbose_name="دوره", blank=True,
                                   null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=PDFCourseSeason, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name="فصل")

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    pdf_file = models.FileField(upload_to="Course/PDFCourse/tutorials", verbose_name="فایل پی‌دی‌اف")

    attachment = models.FileField(upload_to="Course/PDFCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    pages = models.PositiveIntegerField(default=0, verbose_name="تعداد صفحات پی‌دی‌اف")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            pdf_path = self.pdf_file.path

            # Open the PDF file using PyMuPDF
            pdf_document = fitz.open(pdf_path)

            # Get the total number of pages
            total_pages = pdf_document.page_count

            # Update the 'pages' field with the total number of pages
            self.pages = total_pages

        except Exception as e:
            print(f"Error processing PDF: {e}")

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__pdf_course_object'
        verbose_name = 'جزئیات پی‌دی‌اف'
        verbose_name_plural = 'جزئیات پی‌دی‌اف'


class ExamAnswer(models.Model):
    answer_choices = (
        ("1", "گزینه 1"),
        ("2", "گزینه 2"),
        ("3", "گزینه 3"),
        ("4", "گزینه 4"),
    )

    question_number = models.PositiveSmallIntegerField(verbose_name="شماره سوال")

    exam = models.ForeignKey(to="Exam", on_delete=models.CASCADE, verbose_name="آزمون")

    choice_1 = models.CharField(max_length=100, verbose_name="گزینه 1")

    choice_2 = models.CharField(max_length=100, verbose_name="گزینه 2")

    choice_3 = models.CharField(max_length=100, verbose_name="گزینه 3")

    choice_4 = models.CharField(max_length=100, verbose_name="گزینه 4")

    true_answer = models.CharField(max_length=1, choices=answer_choices, verbose_name="گزینه صحیح")

    true_answer_explanation = CKEditor5Field(config_name="extends", blank=True, null=True,
                                             verbose_name="توضیحات اضافه پاسخ صحیح")

    def __str__(self):
        return f"{self.true_answer}"

    class Meta:
        db_table = 'course__exam_answer'
        verbose_name = 'پاسخ آزمون'
        verbose_name_plural = 'پاسخ‌های آزمون'


class Exam(models.Model):
    level_choices_types = (
        ("E", "ساده"),
        ("N", "متوسط"),
        ("H", "پیچیده"),
    )

    video_course_season = models.ForeignKey(to=VideoCourseSeason, on_delete=models.CASCADE, verbose_name="دوره ویدئویی",
                                            blank=True, null=True)

    name = models.CharField(max_length=100, unique=True, verbose_name='نام آزمون')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره آزمون')

    cover_image = models.ImageField(upload_to='Course/Exam/cover_images', verbose_name='عکس کاور')

    level = models.CharField(max_length=1, choices=level_choices_types, verbose_name='میزان سختی', default="N")

    total_duration = models.DurationField(default=0, verbose_name='مدت آزمون')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.total_duration.total_seconds() < 900:
            raise ValidationError(
                message=".زمان آزمون نمی‌تواند کمتر از 15 دقیقه باشد",
                code="invalid_total_duration"
            )

    class Meta:
        db_table = 'course__exam'
        verbose_name = 'آزمون'
        verbose_name_plural = 'آزمون‌ها'


class EnteredExamUser(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name="کاربر")

    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True, verbose_name="آزمون")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        return f"{self.user} - {self.exam.name}"

    class Meta:
        db_table = 'course__entered_exam_user'
        verbose_name = "کاربر شرکت کرده در آزمون"
        verbose_name_plural = "کاربران شرکت کرده در آزمون"


class UserFinalAnswer(models.Model):
    selected_answer_choices = (
        ("1", "گزینه 1"),
        ("2", "گزینه 2"),
        ("3", "گزینه 3"),
        ("4", "گزینه 4"),
    )

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name="کاربر")

    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True, verbose_name="آزمون")

    question_number = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="شماره سوال")

    selected_answer = models.CharField(max_length=10, blank=True, choices=selected_answer_choices, null=True,
                                       verbose_name="گزینه انتخاب شده")

    def __str__(self):
        return f"{self.user.username} - {self.exam.name}"

    class Meta:
        db_table = 'course__user_final_answer'
        verbose_name = "پاسخ نهایی کاربر"
        verbose_name_plural = "پاسخ‌های نهایی کابران"


class BoughtCourse(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    pdf_course = models.ForeignKey(to=PDFCourse, on_delete=models.PROTECT, blank=True, null=True,
                                   verbose_name="دوره پی‌دی‌افی", editable=False)

    video_course = models.ForeignKey(to=VideoCourse, on_delete=models.PROTECT, blank=True, null=True,
                                     verbose_name="دوره ویدئویی", editable=False)

    cost = models.PositiveSmallIntegerField(default=0, verbose_name="قیمت خرید")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = "course__bought_course"
        verbose_name = "دوره خریداری شده"
        verbose_name_plural = "دوره‌های خریداری شده"
