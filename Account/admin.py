from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import CustomUser, OTP, Wallet, Notification, NewsLetter, Follow, FavoriteExam


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
    list_display = ("owner", "fund", "level", "usage_count")

    autocomplete_fields = ("owner",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'created_at', 'mode', 'visibility', 'has_been_read')


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'user')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'followed_at')

    autocomplete_fields = ('follower', 'following')

    search_fields = ('follower__username', 'following__username')


@admin.register(FavoriteExam)
class FavoriteExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'created_at',)
    search_fields = ('user__username', 'exam__name')
