from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import CustomUser, OTP, Wallet, Notification, NewsLetter, Follow, FavoriteVideoCourse, Post
from Home.templatetags.filters import j_date_formatter


class CustomUserAdmin(UserAdmin):
    list_display = ('mobile_phone', 'username', 'is_staff', 'is_superuser', 'date_joined')

    list_editable = ('is_staff', 'is_superuser',)

    search_fields = ('mobile_phone', 'username',)

    readonly_fields = ('date_joined',)

    list_filter = ('is_staff',)

    list_per_page = 50

    ordering = ('-date_joined',)

    search_help_text = "جستجو بر اساس شماره تلفن همراه و نام کاربری"

    filter_horizontal = ()

    fieldsets = ()


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("username", "mobile_phone", "password", "sms_code", "otp_type")


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "formatted_fund", "level",)

    autocomplete_fields = ("user",)

    def formatted_fund(self, obj):
        return "{:,}".format(obj.fund) + " تومان "

    formatted_fund.short_description = "سرمایه"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'admin', 'mode', 'visibility', 'has_been_read', 'formatted_created_at')

    readonly_fields = ('admin',)

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = 'ایجاد شده در تاریخ'

    def save_model(self, request, obj, form, change):
        obj.admin = request.user

        super().save_model(request, obj, form, change)


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'user')


# @admin.register(Follow)
# class FollowAdmin(admin.ModelAdmin):
#     list_display = ('follower', 'following', 'followed_at')
#
#     autocomplete_fields = ('follower', 'following')
#
#     search_fields = ('follower__username', 'following__username')

# @admin.register(FavoriteVideoCourse)
# class FavoriteVideoCourseAdmin(admin.ModelAdmin):
#     list_display = ('user', 'video_course', 'created_at',)
#     search_fields = ('user__username', 'video_course__name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    autocomplete_fields = ('user',)
