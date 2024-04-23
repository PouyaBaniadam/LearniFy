from time import sleep

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Account.models import CustomUser, Wallet
from Cart.mixins import AllowedDiscountCodesOnlyMixin
from Cart.models import Cart, CartItem, Discount, DiscountUsage
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

    def get_queryset(self):
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id', flat=True)

        cart_items = CartItem.objects.filter(cart__user=user)

        total_price_without_discount = 0
        total_price_with_discount = 0

        for item in cart_items:
            if item.video_course:
                total_price_with_discount += item.video_course.price_after_discount
            elif item.pdf_course:
                total_price_with_discount += item.pdf_course.price_after_discount

        for item in cart_items:
            if item.video_course:
                total_price_without_discount += item.video_course.price
            elif item.pdf_course:
                total_price_without_discount += item.pdf_course.price

        wallet = Wallet.objects.get(user=user)
        items_count = CartItem.objects.filter(cart__user=user).count()

        does_cart_items_have_discount = CartItem.objects.filter(
            cart__user=user
        ).filter(
            Q(video_course__has_discount=True) | Q(pdf_course__has_discount=True)
        ).exists()

        context['favorite_video_courses'] = favorite_video_courses
        context['wallet'] = wallet
        context['does_cart_items_have_discount'] = does_cart_items_have_discount
        context['total_price_without_discount'] = total_price_without_discount
        context['total_price_with_discount'] = total_price_with_discount
        context['formatted_total_price_with_discount'] = "{:,}".format(total_price_with_discount)
        context['cost_difference'] = total_price_without_discount - total_price_with_discount
        context['items_count'] = items_count

        return context

    def get_template_names(self):
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if cart_items.exists():
            return ['Cart/cart_items.html']
        else:
            return ['Cart/empty_cart.html']


@method_decorator(csrf_exempt, name='dispatch')
class ApplyDiscount(AllowedDiscountCodesOnlyMixin, View):
    def post(self, request, *args, **kwargs):

        discount_code = request.POST.get("discount_code")
        username = request.user.username
        user = CustomUser.objects.get(username=username)

        discount = Discount.objects.get(code=discount_code)

        cart_items = CartItem.objects.filter(cart__user=user)

        total_price_without_discount = 0
        total_price_with_discount = 0

        for item in cart_items:
            if item.video_course:
                total_price_with_discount += item.video_course.price_after_discount
            elif item.pdf_course:
                total_price_with_discount += item.pdf_course.price_after_discount

        for item in cart_items:
            if item.video_course:
                total_price_without_discount += item.video_course.price
            elif item.pdf_course:
                total_price_without_discount += item.pdf_course.price

        discount_amount = (discount.percent / 100) * total_price_with_discount

        final_price = int(total_price_with_discount - discount_amount)

        return JsonResponse(
            data={
                "message": "کد تخفیف با موفقیت اعمال شد.",
                "final_price": "{:,}".format(final_price),
                "discount_percent": discount.percent
            }
        )


class DeleteItemFromCartItemsPage(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        course_type = kwargs.get("course_type")
        course_id = kwargs.get("course_id")
        username = request.user.username
        user = CustomUser.objects.get(username=username)

        if course_type == "V":
            video_course = VideoCourse.objects.get(id=course_id)
            CartItem.objects.get(cart__user=user, video_course=video_course).delete()

        if course_type == "B":
            pdf_course = PDFCourse.objects.get(id=course_id)
            CartItem.objects.get(cart__user=user, pdf_course=pdf_course).delete()

        return redirect("cart:items")
