from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField

from Account.validators import validate_email
from Course.models import VideoCourse, Exam


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_phone, username=None, email=None, password=None, **extra_fields):
        if not mobile_phone:
            raise ValueError("شماره تلفن الزامی است.")

        if not username:
            raise ValueError("نام کاربری الزامی است.")

        user = self.model(mobile_phone=self.normalize_phone(mobile_phone), username=username,
                          email=self.normalize_email(email) if email else None, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_phone, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("None")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("None")

        return self.create_user(mobile_phone, username, email, password, **extra_fields)

    def normalize_phone(self, mobile_phone):
        return ''.join(filter(str.isdigit, mobile_phone))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=75, unique=True, verbose_name='نام کاربری')

    slug = models.SlugField(unique=True, verbose_name='اسلاگ')

    mobile_phone = models.CharField(max_length=11, unique=True, verbose_name='شمارع تلفن')

    authentication_token = models.UUIDField(unique=True, default=uuid4, verbose_name="یو یو آی دی")

    email = models.EmailField(max_length=254, unique=True, validators=[validate_email], blank=True, null=True,
                              verbose_name='آدرس ایمیل')

    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")

    stars = models.PositiveIntegerField(default=0, verbose_name='تعداد ستاره')

    about_me = models.TextField(blank=True, null=True, verbose_name='درباره من')

    image = models.ImageField(upload_to='Account/Users/profiles/', verbose_name="تصویر پروفایل", blank=True, null=True)

    is_staff = models.BooleanField(default=False, verbose_name='آیا کارمند است؟')

    is_active = models.BooleanField(default=True, verbose_name="آیا فعال است؟")

    date_joined = jDateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ پیوستن')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_phone']

    objects = CustomUserManager()

    def follow(self, user):
        """Follow `user` if not already following."""
        if not self.is_following(user):
            Follow.objects.create(follower=self, following=user)

    def unfollow(self, user):
        """Unfollow `user` if already following."""
        Follow.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        """Check if `self` is following `user`."""
        return Follow.objects.filter(follower=self, following=user).exists()

    def followers_count(self):
        """Return count of followers."""
        return self.followers.count()

    def following_count(self):
        """Return count of followings."""
        return self.following.count()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = slugify(self.username)
        self.username = self.username.lower()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE, verbose_name="فالور")
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE,
                                  verbose_name="فالویینگ")
    followed_at = models.DateTimeField(auto_now_add=True, verbose_name="فالو شده در تاریخ")

    class Meta:
        db_table = 'account__follow'
        verbose_name = "فالو"
        verbose_name_plural = "فالوها"
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username}، {self.following.username} را از تاریخ {self.followed_at} دنبال می‌کند.'


class OTP(models.Model):
    otp_type_choices = (
        ("R", "ثبت نام"),
        ("F", "فراموشی رمز عبور"),
        ("D", "حذف حساب کاربری"),
    )

    username = models.CharField(max_length=75, blank=True, null=True, verbose_name='نام کاربری')

    slug = models.SlugField(blank=True, null=True, verbose_name='اسلاگ')

    mobile_phone = models.CharField(max_length=11, verbose_name='شمارع تلفن')

    password = models.CharField(max_length=100, verbose_name='رمز عبور')

    sms_code = models.CharField(max_length=4, verbose_name='کد تایید')

    uuid = models.UUIDField(blank=True, null=True, verbose_name="یو یو آی دی")

    otp_type = models.CharField(max_length=1, choices=otp_type_choices)

    class Meta:
        verbose_name = "رمز یکبار مصرف"
        verbose_name_plural = "رمزهای یکبار مصرف"

    def __str__(self):
        return f"{self.mobile_phone}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Wallet(models.Model):
    wallet_choices = (
        ("T", "تیتانیومی"),
        ("G", "طلایی"),
        ("S", "نقره‌ای"),
        ("B", "برنزی"),
    )

    owner = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name="wallets", verbose_name="مالک")

    fund = models.PositiveSmallIntegerField(default=0, verbose_name="سرمایه")

    level = models.CharField(max_length=1, choices=wallet_choices, default="B", verbose_name="سطح")

    usage_count = models.PositiveSmallIntegerField(default=0, verbose_name="دفعات استفاده")

    def __str__(self):
        return f"{self.owner.username}"

    class Meta:
        db_table = "account__wallet"
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف‌های پول"


class Notification(models.Model):
    """
    A model for managing user notifications within the application.

    This model provides a flexible and robust framework for creating different
    types of notifications (safe, caution, danger), targeting specific
    user groups (global or private), and offering rich text formatting capabilities
    through the CKEditor5Field.

    Fields:
        title (CharField): A concise and informative notification title.
        message (CKEditor5Field): The notification's detailed content, supporting
        rich text formatting for enhanced user experience.
        users (ManyToManyField): A relationship to link notifications with
        specific CustomUser instances (blank=True allows for global notifications).
        created_at (jDateTimeField): An automatically populated field recording
        the notification's creation timestamp.
        mode (CharField): The notification's severity level (choices from mode_choices).
        visibility (CharField): The notification's target audience (choices from visibility_choices).
    """

    mode_choices = (
        ("S", "Safe"),
        ("C", "Caution"),
        ("D", "Danger"),
    )

    visibility_choices = (
        ("G", "Global"),
        ("P", "Private"),
    )

    uuid = models.UUIDField(default=uuid4, editable=False)

    title = models.CharField(max_length=100)

    message = CKEditor5Field(config_name='extends')

    image = models.ImageField(upload_to="Account/Notification/image", blank=True, null=True)

    users = models.ManyToManyField(to=CustomUser, blank=True)

    created_at = jDateTimeField(auto_now_add=True)

    mode = models.CharField(max_length=1, choices=mode_choices)

    visibility = models.CharField(max_length=1, choices=visibility_choices)

    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'account__notification'
        verbose_name = "اعلانیه"
        verbose_name_plural = "اعلانات"


class NewsLetter(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(max_length=254, verbose_name="آدرس ایمیل", unique=True)

    is_blocked = models.BooleanField(default=False, verbose_name="آیا بلاک شده است؟")

    created_at = jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = 'account__newsletter'
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه‌ها"


class FavoriteExam(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name="کاربر")

    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True, verbose_name="آزمون")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    def __str__(self):
        return f"{self.user} - {self.exam.name}"

    class Meta:
        db_table = 'account__favorite_exam'
        verbose_name = "آزمون مورد علاقه"
        verbose_name_plural = "آزمون‌های مورد علاقه"
