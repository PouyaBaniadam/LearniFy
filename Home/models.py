from django.db import models
from django_jalali.db.models import jDateTimeField


class HeroBanner(models.Model):
    title = models.CharField(max_length=1000, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="1300x400")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__hero_banner"
        verbose_name = "هیرو بنر"
        verbose_name_plural = "هیرو بنرها"


class Banner1(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_1"
        verbose_name = "بنر 1"
        verbose_name_plural = "بنرهای 1"


class Banner2(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="1300x400")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_2"
        verbose_name = "بنر 2"
        verbose_name_plural = "بنرهای 2"


class Banner3(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_3"
        verbose_name = "بنر 3"
        verbose_name_plural = "بنرهای 3"


class Banner4(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_4"
        verbose_name = "بنر 4"
        verbose_name_plural = "بنرهای 4"


class Banner5(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="280x74")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_5"
        verbose_name = "بنر 5"
        verbose_name_plural = "بنرهای 5"


class Banner6(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_6"
        verbose_name = "بنر 6"
        verbose_name_plural = "بنرهای 6"


class Banner7(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_7"
        verbose_name = "بنر 7"
        verbose_name_plural = "بنرهای 7"


class Banner8(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_8"
        verbose_name = "بنر 8"
        verbose_name_plural = "بنرهای 8"


class Banner9(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_9"
        verbose_name = "بنر 9"
        verbose_name_plural = "بنرهای 9"


class Banner10(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_10"
        verbose_name = "بنر 10"
        verbose_name_plural = "بنرهای 10"
