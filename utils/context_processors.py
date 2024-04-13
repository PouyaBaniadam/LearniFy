from Account.models import CustomUser
from Course.filters import ExamFilter
from Course.models import Category, Exam
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


def filter_exams(request):
    exams = Exam.objects.all()

    exam_filter = ExamFilter(request.GET, queryset=exams)

    context = {
        'exam_filter_form': exam_filter.form
    }

    return context
