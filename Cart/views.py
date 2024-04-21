from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Cart.models import Cart, CartItem
from Course.models import VideoCourse, PDFCourse
from Home.mixins import URLStorageMixin


@method_decorator(csrf_exempt, name='dispatch')
class ToggleCart(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_type = request.POST.get('course_type')

        course_id = request.POST.get('course_id')

        cart = Cart.objects.get(user=user)

        if course_type == "V":
            video_course = VideoCourse.objects.get(id=course_id)
            does_cart_item_exists = CartItem.objects.filter(
                cart=cart, video_course=video_course, course_type=course_type
            ).exists()

        if course_type == "B":
            pdf_course = PDFCourse.objects.get(id=course_id)
            does_cart_item_exists = CartItem.objects.filter(
                cart=cart, pdf_course=pdf_course, course_type=course_type
            ).exists()

        if does_cart_item_exists:
            if course_type == "V":
                cart_item = CartItem.objects.filter(
                    cart=cart, video_course=video_course, course_type=course_type
                )
                cart_item.delete()

            if course_type == "B":
                cart_item = CartItem.objects.filter(
                    cart=cart, pdf_course=pdf_course, course_type=course_type
                )
                cart_item.delete()

            return JsonResponse(
                data={'message': 'added',
                      'cart_items_count': cart.items.count()},
                status=200
            )

        else:
            if course_type == "V":
                video_course = VideoCourse.objects.get(id=course_id)
                CartItem.objects.create(
                    cart=cart, course_type=course_type,
                    video_course=video_course
                )

            if course_type == "B":
                pdf_course = PDFCourse.objects.get(id=course_id)
                CartItem.objects.create(
                    cart=cart, course_type=course_type,
                    pdf_course=pdf_course
                )

            return JsonResponse(
                data={'message': 'removed',
                      'cart_items_count': cart.items.count()},
                status=200
            )


class CartItemsView(AuthenticatedUsersOnlyMixin, URLStorageMixin, ListView):
    model = CartItem
    context_object_name = "cart_items"
    template_name = "Cart/cart_items.html"

    def get_queryset(self):
        user = self.request.user

        cart_items = CartItem.objects.filter(cart__user=user)

        print(cart_items)

        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        favorite_video_courses = VideoCourse.objects.filter(
            favoritevideocourse__user=user
        ).values_list('id', flat=True)

        context['favorite_video_courses'] = favorite_video_courses

        return context
