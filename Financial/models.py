import django
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField

from Account.models import CustomUser, Wallet, Notification
from Course.models import VideoCourse, PDFCourse, BoughtCourse
from utils.useful_functions import generate_discount_code, generate_random_integers


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')

    penalty_counter = models.PositiveSmallIntegerField(default=0, verbose_name="تعداد دفعات خطا")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = 'financial__cart'
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class CartItem(models.Model):
    COURSE_CHOICES = (
        ('VID', 'ویدئویی'),
        ('PDF', 'پی‌دی‌افی'),
    )

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='items')

    video_course = models.ForeignKey(to="Course.VideoCourse", on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="دوره ویدئویی")

    pdf_course = models.ForeignKey(to="Course.PDFCourse", on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name="دوره پی‌دی‌افی")

    course_type = models.CharField(max_length=3, choices=COURSE_CHOICES, verbose_name='نوع دوره')

    def __str__(self):
        return f"{self.video_course or self.pdf_course}"

    class Meta:
        db_table = 'financial__cart_item'
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'


class DiscountUsage(models.Model):
    discount = models.ForeignKey(to="Discount", on_delete=models.CASCADE, verbose_name="تخفیف")

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    usage_date = jDateTimeField(auto_now_add=True, verbose_name="تاریخ استفاده")

    def __str__(self):
        return f"{self.user.username} - {self.usage_date}"

    class Meta:
        db_table = 'financial__discount_usage'
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

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="کاربر")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    duration = models.DurationField(help_text="به ثانیه", verbose_name="مدت تخفیف")

    ends_at = models.DateTimeField(blank=True, null=True, editable=False, verbose_name='تاریخ انقضا')

    usage_limits = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(1)],
                                                    verbose_name="محدودیت استفاده به نفر")

    def save(self, *args, **kwargs):
        self.ends_at = timezone.now() + self.duration
        super(Discount, self).save(*args, **kwargs)

    def clean(self):
        if self.duration.total_seconds() < 60:
            raise ValidationError("مدت تخفیف نمی‌تواند کمتر از 60 ثانیه باشد.")

        if self.type == "PV" and self.user is None:
            raise ValidationError(message="در صورت شخصی بودن کد تخفیف، یک کاربر باید انتخاب شده باشد.")

        if self.type == "PV" and self.usage_limits > 1:
            raise ValidationError(message="در صورت شخصی بودن کد تخفیف، محدودیت استفاده باید 1 نفر باشد.")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "financial__discount"
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیفات"


class DepositSlip(models.Model):
    TYPE_CHOICES = (
        ('BUY', 'خرید'),
        ('WAL', 'شارژ کیف پول')
    )

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر", related_name="+")

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, blank=True, null=True, verbose_name="سبد خرید",
                             editable=False)

    admin = models.ForeignKey(to="Account.CustomUser", on_delete=models.PROTECT, blank=True, null=True,
                              verbose_name="ادمین", editable=False, related_name="+")

    receipt = models.ImageField(upload_to="Financial/DepositSlips/receipts", verbose_name="تصویر رسید")

    discount_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد تخفیف")

    total_cost = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ قابل پرداخت", editable=False)

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    difference_cash = models.PositiveBigIntegerField(default=0, verbose_name="ما به تفاوت")

    type = models.CharField(max_length=3, choices=TYPE_CHOICES, verbose_name="نوع")

    tracking_number = models.CharField(max_length=10, default=generate_random_integers, verbose_name="شماره پیگیری")

    is_valid = models.BooleanField(default=False, verbose_name="آیا رسید معتبر است؟")

    is_fake = models.BooleanField(default=False, verbose_name="آیا رسید فیک است؟")

    has_been_finished = models.BooleanField(default=False, verbose_name="کارها انجام شده؟", editable=False)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = self.user

        wallet = Wallet.objects.get(user=user)
        cart = Cart.objects.get(user=user)

        if self.is_fake and self.admin:
            cart.penalty_counter += 1
            cart.save()

            notification = Notification.objects.create(
                admin=self.admin,
                title="رد شدن فیش واریزی",
                message=f'رسید واریزی شما مورد تایید نبود. در صورت وجود هر گونه مشکلی، با تیم پشتیبانی تماس بگیرید.',
                visibility="PV",
                mode="D",
                type="AN",
            )

            notification.users.add(user)

            notification.save()

            self.delete()

        if self.is_valid and self.type == "BUY" and self.has_been_finished is False:
            self.has_been_finished = True
            wallet.charge_wallet(self.difference_cash)
            wallet.difference = self.difference_cash
            wallet.save()

            for item in cart.items.all():
                if item.course_type == "VID":
                    video_course = VideoCourse.objects.get(name=item.video_course.name)
                    video_course.participated_users.add(user)
                    video_course.save()

                    if self.discount_code:
                        discount = Discount.objects.get(code=self.discount_code)
                        discount_amount = (discount.percent / 100) * video_course.price_after_discount

                        BoughtCourse.objects.create(
                            user=user,
                            video_course=video_course,
                            cost=video_course.price_after_discount - discount_amount)

                    else:
                        BoughtCourse.objects.create(
                            user=user,
                            video_course=video_course,
                            cost=video_course.price_after_discount)

                if item.course_type == "PDF":
                    pdf_course = PDFCourse.objects.get(name=item.pdf_course.name)
                    pdf_course.participated_users.add(user)
                    pdf_course.save()

                    if self.discount_code:
                        discount = Discount.objects.get(code=self.discount_code)
                        discount_amount = (discount.percent / 100) * pdf_course.price_after_discount

                        BoughtCourse.objects.create(
                            user=user,
                            pdf_course=pdf_course,
                            cost=pdf_course.price_after_discount - discount_amount)

                    else:
                        BoughtCourse.objects.create(
                            user=user,
                            pdf_course=pdf_course,
                            cost=pdf_course.price_after_discount)

            for item in cart.items.all():
                item.delete()

        if self.is_valid and self.type == "WAL" and self.has_been_finished is False:
            self.has_been_finished = True
            wallet.charge_wallet(self.difference_cash)
            wallet.difference = self.difference_cash
            wallet.save()

        try:
            super().save(*args, **kwargs)
        except django.db.utils.IntegrityError:
            pass

    class Meta:
        db_table = "financial__deposit_slip"
        verbose_name = "فیش واریزی"
        verbose_name_plural = "رسیدهای خرید"


class TempDiscountUsage(models.Model):
    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")

    total_price_with_discount = models.PositiveBigIntegerField(default=0, verbose_name="قیمت نهایی")

    discount = models.ForeignKey(to=Discount, on_delete=models.CASCADE, verbose_name="تخفیف")

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = "financial__temp_discount_usage"
        verbose_name = 'مورد استفاده موقت از کد تخفیف'
        verbose_name_plural = 'موارد استفاده موقت از کد تخفیف'
