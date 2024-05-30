from django.contrib import admin

from Course.models import VideoCourse, VideoCourseObject, Category, VideoCourseSeason, PDFCourseObject, PDFCourse, \
    PDFCourseSeason, BoughtCourse, PDFCourseObjectDownloadedBy, VideoCourseObjectDownloadedBy, PDFExam, PDFExamDetail, \
    PDFExamResult, VideoExam, VideoExamResult, VideoExamDetail
from Home.templatetags.filters import j_date_formatter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name', 'parent')

    autocomplete_fields = ('parent',)

    prepopulated_fields = {'slug': ('name',)}


class VideoCourseObjectDownloadedByInline(admin.TabularInline):
    model = VideoCourseObjectDownloadedBy
    can_delete = False
    readonly_fields = ("user", "formatted_created_at")

    def has_add_permission(self, request, obj):
        return False

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = 'تاریخ ایجاد'


@admin.register(VideoCourseObject)
class VideoCourseObjectAdmin(admin.ModelAdmin):
    list_display = ("title",)

    autocomplete_fields = ('video_course', 'season')

    inlines = (VideoCourseObjectDownloadedByInline,)


class BoughtCourseTabularInline(admin.TabularInline):
    model = BoughtCourse
    readonly_fields = ("user", "formatted_cost", "formatted_created_at")

    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = 'تاریخ خرید'

    def formatted_cost(self, obj):
        return "{:,}".format(obj.cost) + " تومان "

    formatted_cost.short_description = "قیمت خرید"


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
        'holding_status', 'payment_type', 'formatted_price', 'has_discount',
        'discount_percentage', 'formatted_price_after_discount'
    )

    search_fields = ('name',)

    autocomplete_fields = ('teacher', 'category')

    prepopulated_fields = {'slug': ('name',)}

    inlines = (BoughtCourseTabularInline,)

    readonly_fields = ("price_after_discount",)

    def formatted_price_after_discount(self, obj):
        return "{:,}".format(obj.price_after_discount) + " تومان "

    formatted_price_after_discount.short_description = "قیمت بعد از تخفیف"

    def formatted_price(self, obj):
        return "{:,}".format(obj.price) + " تومان "

    formatted_price.short_description = "قیمت"


@admin.register(VideoCourseSeason)
class VideoCourseSeasonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number')

    list_filter = ('course',)

    autocomplete_fields = ('course',)

    search_fields = ('course__name',)


class PDFCourseObjectDownloadedByInline(admin.TabularInline):
    model = PDFCourseObjectDownloadedBy
    can_delete = False
    readonly_fields = ("user", "formatted_created_at")

    def has_add_permission(self, request, obj):
        return False

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = 'تاریخ ایجاد'


@admin.register(PDFCourseObject)
class PDFCourseObjectAdmin(admin.ModelAdmin):
    list_display = ("title",)

    autocomplete_fields = ('pdf_course', 'season')

    readonly_fields = ('pages',)

    inlines = (PDFCourseObjectDownloadedByInline,)


@admin.register(PDFCourse)
class PDFCourseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'holding_status', 'payment_type',
        'formatted_price', 'has_discount', 'discount_percentage',
        'formatted_price_after_discount'
    )

    search_fields = ('name',)

    autocomplete_fields = ('teacher', 'category')

    prepopulated_fields = {'slug': ('name',)}

    inlines = (BoughtCourseTabularInline,)

    readonly_fields = ("price_after_discount",)

    def formatted_price_after_discount(self, obj):
        return "{:,}".format(obj.price_after_discount) + " تومان "

    formatted_price_after_discount.short_description = "قیمت بعد از تخفیف"

    def formatted_price(self, obj):
        return "{:,}".format(obj.price) + " تومان "

    formatted_price.short_description = "قیمت"


@admin.register(PDFCourseSeason)
class PDFCourseSeasonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number')

    list_filter = ('course',)

    autocomplete_fields = ('course',)

    search_fields = ('course__name',)


class PDFExamDetailInline(admin.StackedInline):
    model = PDFExamDetail
    extra = 1


@admin.register(PDFExam)
class PDFExamAdmin(admin.ModelAdmin):
    autocomplete_fields = ("pdf_course_season",)
    inlines = (PDFExamDetailInline,)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PDFExamResult)
class PDFExamResultAdmin(admin.ModelAdmin):
    list_display = ("user", "pdf_exam", "percentage")


class VideoExamDetailInline(admin.StackedInline):
    model = VideoExamDetail
    extra = 1


@admin.register(VideoExam)
class VideoExamAdmin(admin.ModelAdmin):
    autocomplete_fields = ("video_course_season",)
    inlines = (VideoExamDetailInline,)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VideoExamResult)
class VideoExamResultAdmin(admin.ModelAdmin):
    list_display = ("user", "video_exam", "percentage")

# @admin.register(VideoExamTimer)
# class VideoExamTimerAdmin(admin.ModelAdmin):
#     list_display = ("user",)
#
#
# @admin.register(PDFExamTimer)
# class VideoExamTimerAdmin(admin.ModelAdmin):
#     list_display = ("user",)
