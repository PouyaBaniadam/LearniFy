from django.contrib import admin

from Us.models import About, SocialMedia, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile_phone', 'email', 'full_name', 'created_at']
    readonly_fields = ['user', 'mobile_phone', 'email', 'full_name', 'message']
    search_fields = ['user', 'mobile_phone', 'email', 'full_name']


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_card_number', 'bank_card_owner_name']
