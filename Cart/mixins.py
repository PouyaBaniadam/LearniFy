from django.http import JsonResponse
from django.views.generic import View

from Cart.models import Discount, DiscountUsage


class AllowedDiscountCodesOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        discount_code = request.POST.get("discount_code")

        if not discount_code:
            return JsonResponse(
                data={"message": "کد تخفیف بدون مقدار است!"},
                status=404
            )

        try:
            discount = Discount.objects.get(code=discount_code)

            if discount.type == "PU":
                discount_code_usages_count = DiscountUsage.objects.filter(discount=discount).count()

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
