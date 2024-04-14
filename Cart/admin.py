from django.contrib import admin

from Cart.models import Cart, CartItem


class CartItemTabularInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('course_type', 'course_pk')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_method", "total_price", "created_at", "updated_at")

    autocomplete_fields = ("user",)

    readonly_fields = ("payment_method", "total_price")

    inlines = [CartItemTabularInline]
