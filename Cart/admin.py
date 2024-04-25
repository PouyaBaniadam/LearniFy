from django.contrib import admin

from Cart.models import Cart, CartItem, Discount, DiscountUsage, DepositSlip
from Home.templatetags.filters import j_date_formatter


class CartItemTabularInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('course_type', 'video_course', 'pdf_course')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")

    readonly_fields = ("user", "penalty_counter")

    inlines = [CartItemTabularInline]


class DiscountUsageTabularInline(admin.TabularInline):
    model = DiscountUsage
    readonly_fields = ('user', 'discount', 'usage_date')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "percent", "duration", "formatted_created_at", "formatted_ends_at")
    autocomplete_fields = ("individual_user",)
    list_filter = ("type",)
    inlines = [DiscountUsageTabularInline]

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = 'تاریخ شروع'

    def formatted_ends_at(self, obj):
        return j_date_formatter(obj.ends_at)

    formatted_ends_at.short_description = 'تاریخ انقضا'


@admin.register(DepositSlip)
class DepositSlipAdmin(admin.ModelAdmin):
    list_display = ("cart", "is_valid", "admin", "formatted_created_at")
    readonly_fields = ("cart", "tracking_number", "total_cost")
    search_fields = ("cart__user__username", "tracking_number")
    search_help_text = "جستجو بر اساس کاربر یا شماره پیگیری"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        search_term = search_term.strip()
        if search_term:
            queryset |= self.model.objects.filter(cart__user__username__icontains=search_term)
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        if obj.is_fake or obj.is_valid:
            obj.admin = request.user
        super().save_model(request, obj, form, change)

    def formatted_created_at(self, obj):
        return j_date_formatter(obj.created_at)

    formatted_created_at.short_description = "تاریخ ایجاد"
