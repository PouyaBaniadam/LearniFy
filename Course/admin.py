from django.contrib import admin

from Course.models import VideoCourse, VideoCourseObject, Category, VideoCourseSeason, Exam, ExamAnswer, \
    EnteredExamUser, UserFinalAnswer


class UserFinalAnswerInline(admin.StackedInline):
    model = UserFinalAnswer
    extra = 1


class EnteredExamUserInline(admin.StackedInline):
    model = EnteredExamUser
    extra = 1


@admin.register(VideoCourseObject)
class VideoCourseObjectAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
        'holding_status', 'payment_type', 'price', 'has_discount',
        'discount_percentage', 'price_after_discount'
    )

    search_fields = ('name', 'description', 'teacher')

    autocomplete_fields = ('teacher',)

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    prepopulated_fields = {'slug': ('name',)}


@admin.register(VideoCourseSeason)
class VideoCourseSeasonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number')

    list_filter = ('course',)

    search_fields = ('course__name',)


class ExamAnswerInline(admin.StackedInline):
    model = ExamAnswer
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'total_duration', 'category', 'level'
    )

    prepopulated_fields = {'slug': ('name',)}

    inlines = [ExamAnswerInline, UserFinalAnswerInline, EnteredExamUserInline]
