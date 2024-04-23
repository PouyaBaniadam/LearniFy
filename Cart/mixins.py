from django.http import JsonResponse
from django.views.generic import View

from Account.models import CustomUser
from Cart.models import Discount, DiscountUsage


class AllowedDiscountCodesOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        discount_code = request.POST.get("discount_code")
        username = request.user.username

        user = CustomUser.objects.get(username=username)

        if not discount_code:
            return JsonResponse(
                data={"message": "کد تخفیف بدون مقدار است!"},
                status=404
            )

        try:
            discount = Discount.objects.get(code=discount_code)

            if discount.type == "PU":
                discount_code_usages = DiscountUsage.objects.filter(discount=discount)
                discount_code_usages_count = discount_code_usages.count()

                has_user_used_discount = discount_code_usages.filter(
                    user=user, discount=discount
                ).exists()

                if has_user_used_discount:
                    return JsonResponse(
                        data={"message": "این کد تخفیف قبلا توسط شما مورد استفاده قرار گرفته است."},
                        status=400
                    )

                if discount.usage_limits <= discount_code_usages_count:
                    return JsonResponse(
                        data={"message": "این کد تخفیف قابل استفاده نیست."},
                        status=400
                    )

        except Discount.DoesNotExist:
            return JsonResponse(
                data={"message": "چنین کد تخفیفی وجود ندارد!"},
                status=404
            )

        return super().dispatch(request, *args, **kwargs)
