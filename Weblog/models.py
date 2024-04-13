from itertools import chain

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from hitcount.models import HitCount
from star_ratings.models import Rating


class Tag(models.Model):
    name = models.CharField(max_length=75, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'weblog__tags'
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    icon = models.ImageField(upload_to='News/Category/icons/', verbose_name='آیکون', blank=True, null=True)

    cover_image = models.ImageField(upload_to='News/Category/images', verbose_name='تصویر', blank=True, null=True)

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'weblog__category'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'


class Weblog(models.Model):
    author = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='نویسنده',
                               editable=False, related_name='weblogs')

    title = models.CharField(max_length=100, verbose_name='عنوان')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='دسته بندی')

    tags = models.ManyToManyField(to=Tag, verbose_name='تگ‌ها', blank=True, related_name='weblogs')

    content = CKEditor5Field(config_name="extends", verbose_name="محتوا")

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    ratings = GenericRelation(to=Rating, related_query_name='weblogs')

    cover_image = models.ImageField(upload_to='News/News/cover_images', verbose_name='تصویر کاور')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def get_related_weblogs(self, max_results=5):
        """
        Returns related weblogs based on shared tags and categories, ranked by shared tags and then publication date.
        """

        related_weblogs = (
            Weblog.objects.filter(tags__in=self.tags.all())
            .exclude(id=self.id)  # Exclude the current weblog
            .annotate(tag_count=Count('tags'))  # Count shared tags
            .order_by('-tag_count', '-created_at')  # Rank by shared tags, then date
        )

        # If not enough results from tags, try categories:
        if related_weblogs.count() < max_results:
            category_weblogs = Weblog.objects.filter(category=self.category)
            category_weblogs = category_weblogs.exclude(id=self.id)  # Exclude the current weblog
            category_weblogs = category_weblogs.order_by('-created_at')[:max_results - related_weblogs.count()]
            related_weblogs = list(chain(related_weblogs, category_weblogs))  # Convert to list

        return list(set(related_weblogs))[:max_results]  # Ensure related_weblogs is a list before slicing

    def get_latest_weblogs(self):
        latest_weblogs = Weblog.objects.all().order_by('-created_at').exclude(id=self.id)

        return latest_weblogs

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = 'weblog__weblog'
        verbose_name = 'وبلاگ'
        verbose_name_plural = 'وبلاگ‌ها'


class Comment(models.Model):
    weblog = models.ForeignKey(to=Weblog, on_delete=models.CASCADE, verbose_name="وبلاگ",
                               related_name='weblog_comments')

    user = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر", related_name="user_weblog_comments")

    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, verbose_name="والد", blank=True, null=True,
                               related_name="replies")

    text = models.TextField(max_length=1000, verbose_name="متن")

    likes = models.ManyToManyField(to="Account.CustomUser", verbose_name="لایک‌ها",
                                   related_name="weblog_comments_likes",
                                   blank=True)

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='به‌روز‌رسانی شده در تاریخ')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = 'weblog__comment'
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
        ordering = ('-created_at',)
