from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField

from Account.models import CustomUser


class Message(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, related_name='messages', blank=True,
                             null=True, verbose_name="کاربر")

    mobile_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره تلفن")

    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="آدرس ایمیل")

    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام و نام خانوادگی")

    can_be_shown = models.BooleanField(default=False, verbose_name="مجوز نشان داده شدن دارد؟")

    message = models.TextField(max_length=500, verbose_name="پیام")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        if self.user:
            return f"{self.user.username}"

        else:
            sender_name = ", ".join(filter(None, [self.full_name, self.mobile_phone, self.email]))
            return f"{sender_name}" if sender_name else "ناشناس"

    class Meta:
        db_table = 'us__message'
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'


class SocialMedia(models.Model):
    phone_1 = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن اول')

    phone_2 = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن دوم')

    telegram_url = models.URLField(blank=True, null=True, verbose_name='لینک تلگرام')

    telegram_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                      verbose_name='آیکون تلگرام')

    telegram_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='شماره تلگرام')

    whats_App_url = models.URLField(blank=True, null=True, verbose_name='لینک واتس‌اپ')

    whats_App_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                       verbose_name='آیکون واتس‌اپ')

    whats_App_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='شماره واتس اپ')

    linkedIn_url = models.URLField(blank=True, null=True, verbose_name='لینک لینکدین')

    linkedIn_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                      verbose_name='آیکون لینکدین')

    pinterest_url = models.URLField(blank=True, null=True, verbose_name='لینک پینترست')

    pinterest_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                       verbose_name='آیکون پینترست')

    instagram_url = models.URLField(blank=True, null=True, verbose_name='لینک اینستاگرام')

    instagram_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                       verbose_name='آیکون اینستاگرام')

    twitter_url = models.URLField(blank=True, null=True, verbose_name='لینک توییتر')

    twitter_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                     verbose_name='آیکون توییتر')

    facebook_url = models.URLField(blank=True, null=True, verbose_name='لینک فیس‌بوک')

    facebook_icon = models.ImageField(upload_to="Us/SocialMedia/icons", blank=True, null=True,
                                      verbose_name='آیکون فیس‌بوک')

    def __str__(self):
        return f"شبکه اجتماعی"

    class Meta:
        db_table = 'us__social_media'
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = 'شبکه‌های اجتماعی'


class AboutUs(models.Model):
    name = models.CharField(max_length=75, verbose_name='نام')

    short_description = CKEditor5Field(config_name="extends", verbose_name="توضیح مختصر")

    what_we_do = CKEditor5Field(config_name="extends", verbose_name="چی کار می‌کنیم")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'us__about_us'
        verbose_name = 'درباره'
        verbose_name_plural = 'درباره ما'
