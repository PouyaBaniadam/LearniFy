from Account.models import CustomUser
from Cart.models import Cart
from Course.filters import VideoCourseFilter, PDFCourseFilter
from Course.models import Category, Exam, VideoCourse, PDFCourse
from Us.models import SocialMedia, AboutUs


def social_media(request):
    social_media = SocialMedia.objects.last()
    about_us = AboutUs.objects.last()

    context = {
        'social_media': social_media,
        'about_us': about_us,
    }

    return context


def custom_user_info(request):
    user = request.user

    if user.is_authenticated:
        custom_user = CustomUser.objects.get(username=user.username)

        return {
            'custom_user': custom_user
        }

    else:
        return {
            'custom_user': None
        }


def filter_categories(request):
    categories = Category.objects.all()

    context = {
        'filter_categories': categories
    }

    return context


def filter_courses(request):
    video_courses = VideoCourse.objects.all()
    pdf_courses = PDFCourse.objects.all()

    video_course_filter = VideoCourseFilter(request.GET, queryset=video_courses)
    pdf_course_filter = PDFCourseFilter(request.GET, queryset=pdf_courses)

    context = {
        'video_course_filter_form': video_course_filter.form,
        'pdf_course_filter_form': pdf_course_filter.form
    }

    return context


def cart_items_count(request):
    user = request.user
    try:
        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
            count = cart.items.count()

        else:
            count = 0

    except Cart.DoesNotExist:
        count = 0

    context = {
        'cart_items_count': count
    }

    return context
