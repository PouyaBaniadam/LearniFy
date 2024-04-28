from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField


class IntroBanner(models.Model):
    title = models.CharField(max_length=1000, verbose_name="تیتر")

    description = CKEditor5Field(config_name="extends", verbose_name='توضیحات')

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="1300x400")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__intro_banner"
        verbose_name = "هیرو بنر"
        verbose_name_plural = "هیرو بنرها"
