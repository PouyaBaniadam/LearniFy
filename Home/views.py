from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from Course.models import VideoCourse, Exam, PDFCourse
from Home.mixins import URLStorageMixin
from Home.models import HeroBanner, Banner1, Banner2, Banner3
from News.models import News
from Us.models import Message
from Weblog.models import Weblog


class HomeView(URLStorageMixin, TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user

        latest_video_courses = VideoCourse.objects.values("teacher__image",
                                                          "id",
                                                          "category__name",
                                                          "category__slug",
                                                          "cover_image",
                                                          "holding_status",
                                                          "teacher__username",
                                                          "teacher__slug",
                                                          "teacher__full_name",
                                                          "total_sessions",
                                                          "total_seasons",
                                                          "has_discount",
                                                          "payment_type",
                                                          "price",
                                                          "slug",
                                                          "price_after_discount",
                                                          "total_duration",
                                                          "name",
                                                          "holding_status").order_by('-created_at').filter(
            Q(holding_status="F") | Q(holding_status="IP"))[:6]

        latest_pdf_courses_1 = PDFCourse.objects.values(
            "teacher__image",
            "id",
            "category__name",
            "category__slug",
            "cover_image",
            "holding_status",
            "teacher__username",
            "teacher__slug",
            "teacher__full_name",
            "total_sessions",
            "total_seasons",
            "has_discount",
            "payment_type",
            "price",
            "slug",
            "price_after_discount",
            "total_pages",
            "name",
            "holding_status"
        ).order_by('-created_at')[:2]

        latest_pdf_courses_2 = PDFCourse.objects.values(
            "teacher__image",
            "id",
            "category__name",
            "category__slug",
            "cover_image",
            "holding_status",
            "teacher__username",
            "teacher__slug",
            "teacher__full_name",
            "total_sessions",
            "total_seasons",
            "has_discount",
            "payment_type",
            "price",
            "slug",
            "price_after_discount",
            "total_pages",
            "name",
            "holding_status"
        ).order_by('-created_at')[2:4]

        latest_news = News.objects.all().order_by('-created_at')

        latest_weblogs = Weblog.objects.all().order_by('-created_at')

        hero_banners = HeroBanner.objects.filter(can_be_shown=True).order_by('-created_at')

        banner_1 = Banner1.objects.filter(can_be_shown=True).order_by('-created_at')[:2]

        banner_2 = Banner2.objects.filter(can_be_shown=True).last()

        banner_3 = Banner3.objects.filter(can_be_shown=True).order_by('-created_at')[:2]

        attitudes = Message.objects.filter(can_be_shown=True).order_by('-created_at')

        if user.is_authenticated:
            favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id',
                                                                                                            flat=True)
        else:
            favorite_video_courses = []

        context['latest_video_courses'] = latest_video_courses  # Is a queryset
        context['latest_pdf_courses_1'] = latest_pdf_courses_1  # Is a queryset
        context['latest_pdf_courses_2'] = latest_pdf_courses_2  # Is a queryset
        context['latest_news'] = latest_news  # Is a queryset
        context['latest_weblogs'] = latest_weblogs  # Is a queryset
        context['hero_banners'] = hero_banners  # Is a queryset
        context['banner_1'] = banner_1  # Is a queryset
        context['banner_2'] = banner_2  # Is a single object
        context['banner_3'] = banner_3  # Is a queryset
        context['attitudes'] = attitudes  # Is a queryset
        context['favorite_video_courses'] = favorite_video_courses  # Is a queryset

        return context


class SearchView(TemplateView):
    template_name = "Home/search_result.html"

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')

        weblog_result = Weblog.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q))

        news_result = News.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q))

        video_course_result = VideoCourse.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q))

        exams_result = Exam.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q))

        context = {
            'weblog_result': weblog_result,
            'news_result': news_result,
            'exams_result': exams_result,
            'video_course_result': video_course_result,
        }

        return render(request=request, template_name=self.template_name, context=context)
