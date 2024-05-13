from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from Course.models import VideoCourse, PDFCourse
from Home.mixins import URLStorageMixin
from Home.models import IntroBanner
from News.models import News
from Us.models import Message, WhyUs
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
                                                          "has_discount",
                                                          "payment_type",
                                                          "price",
                                                          "slug",
                                                          "price_after_discount",
                                                          "name",
                                                          "holding_status"
                                                          ).order_by('-created_at')[:6]

        latest_pdf_courses = PDFCourse.objects.values(
            "id",
            "category__name",
            "category__slug",
            "cover_image",
            "holding_status",
            "teacher__image",
            "teacher__slug",
            "teacher__username",
            "teacher__full_name",
            "has_discount",
            "payment_type",
            "price",
            "slug",
            "price_after_discount",
            "name",
            "holding_status",
            "what_we_will_learn",
        ).order_by('-created_at')[:6]

        intro_banner = IntroBanner.objects.first()

        latest_news = News.objects.all().order_by('-created_at')
        latest_weblogs = Weblog.objects.all().order_by('-created_at')

        attitudes = Message.objects.filter(can_be_shown=True).order_by('-created_at')

        favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)
        favorite_pdf_courses =  PDFCourse.favorite_pdf_list(self, user=user)

        why_us_part_1 = WhyUs.objects.values_list("id", "title", "icon")
        why_us_part_2 = WhyUs.objects.values_list("id", "image", "description")

        try:
            default_why_us_id = WhyUs.objects.first().id
        except AttributeError:
            default_why_us_id = 1

        context['latest_video_courses'] = latest_video_courses  # Is a queryset
        context['latest_pdf_courses'] = latest_pdf_courses  # Is a queryset
        context['latest_news'] = latest_news  # Is a queryset
        context['latest_weblogs'] = latest_weblogs  # Is a queryset
        context['intro_banner'] = intro_banner  # Is a single object
        context['attitudes'] = attitudes  # Is a queryset
        context['favorite_video_courses'] = favorite_video_courses  # Is a queryset
        context['favorite_pdf_courses'] = favorite_pdf_courses  # Is a queryset
        context['why_us_part_1'] = why_us_part_1  # Is a queryset
        context['why_us_part_2'] = why_us_part_2  # Is a queryset
        context['default_why_us_id'] = default_why_us_id  # Is a single object

        return context


class SearchView(TemplateView):
    template_name = "Home/search_result.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        favorite_video_courses = []
        favorite_pdf_courses = []

        q = request.GET.get('q')
        selected_category = request.GET.get('category')

        if selected_category == "weblog":
            result_type = "weblog"
            result = Weblog.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(category__name__icontains=q)
            )

        elif selected_category == "news":
            result_type = "news"
            result = News.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(category__name__icontains=q)
            )

        elif selected_category == "video_course":
            favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

            result_type = "video_course"
            result = VideoCourse.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(what_we_will_learn__icontains=q) |
                Q(category__name__icontains=q)
            )

        elif selected_category == "pdf_course":
            favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

            result_type = "pdf_course"
            result = PDFCourse.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(what_we_will_learn__icontains=q) |
                Q(category__name__icontains=q)
            )

        else:  # Default search category is pdf courses
            favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

            result_type = "pdf_course"
            result = PDFCourse.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(what_we_will_learn__icontains=q) |
                Q(category__name__icontains=q)
            )

        context = {
            "favorite_video_courses": favorite_video_courses,
            "favorite_pdf_courses": favorite_pdf_courses,
            "result_type": result_type,
            "result": result
        }

        return render(request=request, template_name=self.template_name, context=context)
