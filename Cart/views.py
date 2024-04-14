from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from Cart.models import Cart, CartItem


@method_decorator(csrf_exempt, name='dispatch')
class ToggleCart(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_type = request.POST.get('course_type')

        course_id = request.POST.get('course_id')

        cart = Cart.objects.get(user=user)

        does_cart_item_exists = CartItem.objects.filter(
            cart=cart, course_pk=course_id, course_type=course_type
        ).exists()

        if does_cart_item_exists:
            cart_item = CartItem.objects.filter(
                cart=cart, course_pk=course_id, course_type=course_type
            )

            cart_item.delete()

            return JsonResponse(
                {'message': 'added',
                 'cart_items_count': cart.items.count()},
                status=200
            )

        else:
            CartItem.objects.create(
                cart=cart, course_pk=course_id, course_type=course_type
            )

            return JsonResponse(
                {'message': 'removed',
                 'cart_items_count': cart.items.count()},
                status=200
            )
