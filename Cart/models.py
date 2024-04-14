from django.db import models

from Account.models import CustomUser


class Cart(models.Model):
    PAYMENT_CHOICES = (
        ('PP', 'درکاه پرداخت'),  # PayPort
        ('CT', 'انتقال به کارت'),  # CardTransfer
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')

    payment_method = models.CharField(max_length=2, choices=PAYMENT_CHOICES, blank=True, null=True,
                                      verbose_name='نحوه پرداخت')

    total_price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت نهایی')

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

    course_type = models.CharField(max_length=1, choices=COURSE_CHOICES, verbose_name='نوع')

    course_pk = models.PositiveSmallIntegerField(verbose_name='آیدی دوره')

    def __str__(self):
        return f"{self.course_pk} - {self.course_type}"

    class Meta:
        db_table = 'cart__cart_item'
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'
