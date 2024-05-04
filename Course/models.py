import string

import fitz
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import Sum
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from moviepy.editor import VideoFileClip
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='والد')

    icon = models.ImageField(upload_to='Course/Category/icons/', verbose_name='آیکون', blank=True, null=True)

    cover_image = models.ImageField(upload_to='Course/Category/images', verbose_name='تصویر', blank=True, null=True)

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

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

    what_we_will_learn = models.TextField(max_length=250, verbose_name='چی یاد میگیریم؟')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.SET_DEFAULT, default=1,
                                verbose_name='مدرس', related_name='teacher_video_courses')

    cover_image = models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')

    introduction_video = models.FileField(upload_to='Course/VideoCourse/introduction_video',
                                          validators=[FileExtensionValidator(['mp4', 'mkv'])],
                                          verbose_name='فیلم مقدمه', help_text="فرمت‌‌های mp4 و mkv")

    holding_status = models.CharField(max_length=2, choices=HOLDING_STATUS_CHOICES, verbose_name='وضعیت دوره',
                                      default='NS')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    coefficient_number = models.PositiveSmallIntegerField(default=1, verbose_name="ضریب",
                                                          validators=[MinValueValidator(1), MaxValueValidator(4)],
                                                          help_text="یک عدد صحیح بین 1 تا 4")

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_video_courses', editable=False)

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, default='F', verbose_name='نوع دوره')

    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveBigIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')

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

    def calculate_total_duration(self):
        total_duration = self.videocourseobject_set.aggregate(total_duration=Sum('duration'))['total_duration']

        if total_duration is None:
            total_duration = 0

        return total_duration

    def favorite_video_list(self, user):
        favorites = []
        if user.is_authenticated:
            favorites = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id', flat=True)

        return favorites

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


class VideoCourseObjectDownloadedBy(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    video_course_object = models.ForeignKey(to="VideoCourseObject", on_delete=models.CASCADE,
                                            verbose_name="جزئیات ویدئو")

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایحاد')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = 'course__video_course_object_downloaded_by'
        verbose_name = 'دانلود شده توسط'
        verbose_name_plural = 'دانلود شده توسط'


class VideoCourseObject(models.Model):
    video_course = models.ForeignKey(VideoCourse, on_delete=models.PROTECT, verbose_name="دوره", blank=True,
                                     null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    download_file_name = models.CharField(max_length=50, verbose_name="نام فایل دانلودی",
                                          help_text="فقط حروف انگلیسی و ارقام لاتین")

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=VideoCourseSeason, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name="فصل")

    session = models.PositiveSmallIntegerField(default=1, verbose_name="قسمت")

    video_file = models.FileField(upload_to="Course/VideoCourse/tutorials",
                                  validators=[FileExtensionValidator(['mp4', 'mkv'])],
                                  verbose_name="فایل ویدئو", help_text="فرمت‌‌های mp4 و mkv")

    attachment = models.FileField(upload_to="Course/VideoCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    duration = models.PositiveIntegerField(default=0, verbose_name="زمان فیلم")

    def __str__(self):
        return f"{self.title}"

    def clean(self, *args, **kwargs):
        allowed_characters = string.ascii_letters + string.digits + "-_"

        for letter in self.download_file_name:
            if letter not in allowed_characters:
                raise ValidationError(message="نام فایل دانلودی فقط می‌‌تواند شامل حروف انگلیسی و ارقام باشد.")

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
        verbose_name = 'قسمت  دوره ویدئویی'
        verbose_name_plural = 'قسمت‌‌های دوره ویدئویی'


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

    what_we_will_learn = models.TextField(max_length=250, verbose_name='چی یاد میگیریم؟')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='مدرس',
                                related_name='teacher_pdf_courses')

    cover_image = models.ImageField(upload_to='Course/PDFCourse/cover_images', verbose_name='عکس کاور')

    introduction_pdf = models.FileField(upload_to='Course/PDFCourse/introduction_pdf',
                                        validators=[FileExtensionValidator(['pdf'])],
                                        verbose_name='پی‌دی‌اف مقدمه', help_text="فقط PDF")

    holding_status = models.CharField(max_length=2, choices=HOLDING_STATUS_CHOICES, verbose_name='وضعیت دوره',
                                      default='NS')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    coefficient_number = models.PositiveSmallIntegerField(default=1, verbose_name="ضریب",
                                                          validators=[MinValueValidator(1), MaxValueValidator(4)],
                                                          help_text="یک عدد صحیح بین 1 تا 4")

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده',
                                                related_name='user_pdf_courses', editable=False)

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, default='F', verbose_name='نوع دوره')

    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveBigIntegerField(default=0, editable=False, verbose_name='قیمت بعد از تخفیف')

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

    def calculate_total_pages(self):
        total_pages = self.pdfcourseobject_set.aggregate(total_pages=Sum('pages'))['total_pages']

        if total_pages is None:
            total_pages = 0

        return total_pages

    def favorite_pdf_list(self, user):
        favorites = []
        if user.is_authenticated:
            favorites = PDFCourse.objects.filter(favoritepdfcourse__user=user).values_list('id', flat=True)

        return favorites

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


class PDFCourseObjectDownloadedBy(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    pdf_course_object = models.ForeignKey(to="PDFCourseObject", on_delete=models.CASCADE,
                                          verbose_name="جزئیات پی‌دی‌اف")

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایحاد')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = 'course__pdf_course_object_downloaded_by'
        verbose_name = 'دانلود شده توسط'
        verbose_name_plural = 'دانلود شده توسط'


class PDFCourseObject(models.Model):
    pdf_course = models.ForeignKey(PDFCourse, on_delete=models.PROTECT, verbose_name="دوره", blank=True,
                                   null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    download_file_name = models.CharField(max_length=50, verbose_name="نام فایل دانلودی",
                                          help_text="فقط حروف انگلیسی و ارقام لاتین")

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=PDFCourseSeason, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name="فصل")

    session = models.PositiveSmallIntegerField(default=1, verbose_name="قسمت")

    pdf_file = models.FileField(upload_to="Course/PDFCourse/tutorials", validators=[FileExtensionValidator(['pdf'])],
                                verbose_name="فایل پی‌دی‌اف", help_text="فقط PDF")

    attachment = models.FileField(upload_to="Course/PDFCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    pages = models.PositiveIntegerField(default=0, verbose_name="تعداد صفحات پی‌دی‌اف")

    def __str__(self):
        return f"{self.title}"

    def clean(self, *args, **kwargs):
        allowed_characters = string.ascii_letters + string.digits + "-_"

        for letter in self.download_file_name:
            if letter not in allowed_characters:
                raise ValidationError(message="نام فایل دانلودی فقط می‌‌تواند شامل حروف انگلیسی و ارقام باشد.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pdf_path = self.pdf_file.path

        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(pdf_path)

        # Get the total number of pages
        total_pages = pdf_document.page_count

        # Update the 'pages' field with the total number of pages
        self.pages = total_pages

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course__pdf_course_object'
        verbose_name = 'قسمت  دوره پی‌دی‌افی'
        verbose_name_plural = 'قسمت‌‌های دوره پی‌دی‌افی'


class BoughtCourse(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="کاربر")

    pdf_course = models.ForeignKey(to=PDFCourse, on_delete=models.PROTECT, blank=True, null=True,
                                   verbose_name="دوره پی‌دی‌افی", editable=False)

    video_course = models.ForeignKey(to=VideoCourse, on_delete=models.PROTECT, blank=True, null=True,
                                     verbose_name="دوره ویدئویی", editable=False)

    cost = models.PositiveBigIntegerField(default=0, verbose_name="قیمت خرید", editable=False)

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = "course__bought_course"
        verbose_name = "دوره خریداری شده"
        verbose_name_plural = "دوره‌های خریداری شده"
