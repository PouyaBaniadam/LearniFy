from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField

from Account.models import CustomUser, Wallet
from utils.useful_functions import generate_discount_code, generate_random_integers


class Cart(models.Model):
    PAYMENT_CHOICES = (
        ('PP', 'درکاه پرداخت'),  # PayPort
        ('CT', 'انتقال به کارت'),  # CardTransfer
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')

    payment_method = models.CharField(max_length=2, choices=PAYMENT_CHOICES, blank=True, null=True,
                                      verbose_name='نحوه پرداخت')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = 'cart__cart'
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class CartItem(models.Model):
    COURSE_CHOICES = (
        ('V', 'ویدئویی'),
        ('B', 'کتابی'),
    )

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='items')

    video_course = models.ForeignKey(to="Course.VideoCourse", on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="دوره ویدئویی")

    pdf_course = models.ForeignKey(to="Course.PDFCourse", on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name="دوره پی‌دی‌افی")

    course_type = models.CharField(max_length=1, choices=COURSE_CHOICES, verbose_name='نوع')

    def __str__(self):
        return f"{self.video_course or self.pdf_course} - {self.course_type}"

    class Meta:
        db_table = 'cart__cart_item'
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'


class DiscountUsage(models.Model):
    discount = models.ForeignKey(to="Discount", on_delete=models.CASCADE, verbose_name="تخفیف")

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    usage_date = models.DateTimeField(verbose_name="تاریخ استفاده")

    def __str__(self):
        return f"{self.user.username} - {self.usage_date}"

    class Meta:
        db_table = 'cart__discount_usage'
        verbose_name = 'مورد استفاده کد تخفیف'
        verbose_name_plural = 'موارد استفاده کد تخفیف'


class Discount(models.Model):
    DISCOUNT_CHOICES = (
        ("PU", "عمومی"),
        ("PV", "شخصی"),
    )

    code = models.CharField(max_length=10, verbose_name="کد تخفیف", default=generate_discount_code, unique=True)

    percent = models.PositiveSmallIntegerField(verbose_name="درصد تخفیف", validators=[MaxValueValidator(99),
                                                                                      MinValueValidator(1)])

    description = CKEditor5Field(config_name="extends", blank=True, null=True, verbose_name='درباره تخفیف')

    type = models.CharField(max_length=2, choices=DISCOUNT_CHOICES, verbose_name="نوع تخفیف")

    individual_user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="کاربر")

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    duration = models.DurationField(help_text="به ثانیه", verbose_name="مدت تخفیف")

    ends_at = jDateTimeField(blank=True, null=True, editable=False, verbose_name='تاریخ انقضا')

    usage_limits = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(1)],
                                                    verbose_name="محدودیت استفاده به نفر")

    def save(self, *args, **kwargs):
        self.ends_at = timezone.now() + self.duration
        super(Discount, self).save(*args, **kwargs)

    def clean(self):
        if self.duration.total_seconds() < 60:
            raise ValidationError("مدت تخفیف نمی‌تواند کمتر از 60 ثانیه باشد.")

        if self.type == "PV" and self.individual_user is None:
            raise ValidationError(message="در صورت شخصی بودن کد تخفیف، یک کاربر باید انتخاب شده باشد.")

        if self.type == "PV" and self.usage_limits > 1:
            raise ValidationError(message="در صورت شخصی بودن کد تخفیف، محدودیت استفاده باید 1 نفر باشد.")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "cart__discount"
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیفات"


class DepositSlip(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.PROTECT, verbose_name="سبد خرید")

    admin = models.ForeignKey(to="Account.CustomUser", on_delete=models.PROTECT, blank=True, null=True,
                              verbose_name="ادمین", editable=False)

    receipt = models.ImageField(upload_to="Cart/DepositSlips/receipts", verbose_name="تصویر رسید")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    difference_cash = models.PositiveSmallIntegerField(default=0, verbose_name="ما به تفاوت")

    tracking_number = models.CharField(max_length=10, default=generate_random_integers, verbose_name="شماره پیگیری")

    is_valid = models.BooleanField(default=False, verbose_name="آیا معتبر است؟")

    def __str__(self):
        return f"{self.cart.user}"

    def save(self, *args, **kwargs):
        if self.is_valid:
            user = self.cart.user
            wallet = Wallet.objects.get(user=user)

            wallet.fund += self.difference_cash
            wallet.save()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "cart__deposit_slip"
        verbose_name = "رسید خرید"
        verbose_name_plural = "رسیدهای خرید"
