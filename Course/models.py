from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from moviepy.editor import VideoFileClip

from Home.validators import english_language_validator


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
    course_payment_types = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    course_status_types = (
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

    status = models.CharField(max_length=2, choices=course_status_types, verbose_name='وضعیت دوره', default='NS')

    total_seasons = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل‌ها')

    total_sessions = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name='تعداد قسمت‌ها')

    total_duration = models.PositiveIntegerField(default=0, verbose_name='مدت دوره')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_video_courses')

    type = models.CharField(max_length=1, choices=course_payment_types, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت بعد از تخفیف')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.type == "F":
            self.price = self.price_after_discount = self.discount_percentage = self.has_discount = 0

        if self.has_discount:
            self.price_after_discount = self.price - (self.price * (self.discount_percentage / 100))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__video_course'
        verbose_name = 'دوره ویدئویی'
        verbose_name_plural = 'دوره‌های ویدئویی'


class VideoSeason(models.Model):
    number = models.PositiveSmallIntegerField(default=1, verbose_name="شماره فصل")

    name = models.CharField(max_length=75, verbose_name="اسم فصل")

    course = models.ForeignKey(to=VideoCourse, on_delete=models.CASCADE, verbose_name="دوره")

    def __str__(self):
        return f"{self.course.name} - {self.name} - {self.number}"

    class Meta:
        db_table = 'course__video_season'
        verbose_name = 'فصل ویدئو'
        verbose_name_plural = 'فصل‌های ویدئو'


class VideoCourseObject(models.Model):
    video_course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE, verbose_name="دوره", blank=True,
                                     null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=VideoSeason, on_delete=models.CASCADE, blank=True, null=True, verbose_name="فصل")

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    video_file = models.FileField(upload_to="Course/VideoCourse/tutorials", verbose_name="فایل ویدئو", blank=True,
                                  null=True)

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


class ExamSection(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")

    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name="اسلاگ")

    description = CKEditor5Field(config_name="extends", verbose_name="توضیحات", blank=True, null=True)

    coefficient = models.SmallIntegerField(default=1, verbose_name="ضریب")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'course__exam_section'
        verbose_name = 'بخش آزمون'
        verbose_name_plural = 'بخش‌های آزمون'


class ExamUnit(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")

    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name="اسلاگ")

    description = CKEditor5Field(config_name="extends", verbose_name="توضیحات", blank=True, null=True)

    coefficient = models.SmallIntegerField(default=1, verbose_name="ضریب درس")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'course__exam_unit'
        verbose_name = 'درس آزمون'
        verbose_name_plural = 'دروس آزمون'


class ExamAnswer(models.Model):
    answer_choices = (
        ("1", "گزینه 1"),
        ("2", "گزینه 2"),
        ("3", "گزینه 3"),
        ("4", "گزینه 4"),
    )

    question_number = models.PositiveSmallIntegerField(verbose_name="شماره سوال")

    exam = models.ForeignKey(to="Exam", on_delete=models.CASCADE, verbose_name="آزمون")

    section = models.ForeignKey(to="ExamSection", on_delete=models.CASCADE, verbose_name="بخش")

    unit = models.ForeignKey(to="ExamUnit", on_delete=models.CASCADE, verbose_name="درس")

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
    exam_payment_types = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    level_choices_types = (
        ("E", "ساده"),
        ("N", "متوسط"),
        ("H", "پیچیده"),
    )

    # video_course = models.ForeignKey(to=VideoCourse, on_delete=models.CASCADE, verbose_name="دوره ویدئویی", blank=True,
    #                                  null=True)

    designer = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="طراح", editable=False)

    name = models.CharField(max_length=100, unique=True, verbose_name='نام آزمون')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    questions_file = models.FileField(upload_to='Course/Exam/pdf', verbose_name='فایل سوالات آزمون',
                                      validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    is_downloading_question_files_allowed = models.BooleanField(default=True,
                                                                verbose_name='آیا دانلود سوالات آزمون مجاز است؟')

    question_file_name = models.CharField(max_length=100, unique=True, verbose_name='نام فایل', help_text="فقط انگلیسی",
                                          validators=[english_language_validator])

    description = CKEditor5Field(config_name="extends", verbose_name='درباره آزمون')

    cover_image = models.ImageField(upload_to='Course/Exam/cover_images', verbose_name='عکس کاور')

    level = models.CharField(max_length=1, choices=level_choices_types, verbose_name='میزان سختی', default="N")

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_exams')

    type = models.CharField(max_length=1, choices=exam_payment_types, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت بعد از تخفیف')

    total_duration = models.DurationField(default=0, verbose_name='مدت آزمون')

    is_entrance_allowed = models.BooleanField(default=True, verbose_name='آیا ورود به آزمون مجاز است؟')

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

    def save(self, *args, **kwargs):
        if self.type == "F":
            self.price = self.price_after_discount = self.discount_percentage = self.has_discount = 0

        if self.has_discount:
            self.price_after_discount = self.price - (self.price * (self.discount_percentage / 100))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__exam'
        verbose_name = 'آزمون'
        verbose_name_plural = 'آزمون‌ها'


class DownloadedQuestionFile(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name="کاربر")

    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True, verbose_name="آزمون")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        return f"{self.user.username} - {self.exam.name}"

    class Meta:
        db_table = 'course__downloaded_question_file'
        verbose_name = "فایل دانلود شده"
        verbose_name_plural = "فایل‌های دانلود شده"


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


class UserTempAnswer(models.Model):
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
        db_table = 'course__user_temp_answer'
        verbose_name = "پاسخ موقت کاربر"
        verbose_name_plural = "پاسخ‌های موقت کابران"
