from django.contrib import admin

from Cart.models import Cart, CartItem, DiscountCode


class CartItemTabularInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('course_type', 'video_course', 'pdf_course')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_method", "total_price", "created_at", "updated_at")

    autocomplete_fields = ("user",)

    readonly_fields = ("payment_method", "total_price")

    inlines = [CartItemTabularInline]


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "ends_at")
