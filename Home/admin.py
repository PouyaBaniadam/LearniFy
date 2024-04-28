from django.contrib import admin

from Home.models import IntroBanner


@admin.register(IntroBanner)
class IntroBannerBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)
