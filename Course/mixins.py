from datetime import datetime

import pytz
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from Account.models import CustomUser
from Course.models import PDFCourse, VideoCourse
from utils.useful_functions import get_time_difference


class ParticipatedUsersPDFCoursesOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        pdf_course = PDFCourse.objects.get(slug=slug)

        if user != pdf_course.teacher:
            can_user_participate = PDFCourse.objects.filter(
                slug=slug,
                participated_users=user
            ).exists()

            if not can_user_participate:
                redirect_url = request.session.get('current_url')

                messages.error(request, f"شما مجوز دسترسی به این بخش را ندارید!")

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)


class ParticipatedUsersVideoCoursesOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        video_course = VideoCourse.objects.get(slug=slug)

        if user != video_course.teacher:
            can_user_participate = VideoCourse.objects.filter(
                slug=slug,
                participated_users=user
            ).exists()

            if not can_user_participate:
                redirect_url = request.session.get('current_url')

                messages.error(request, f"شما مجوز دسترسی به این بخش را ندارید!")

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)


class RedirectToPDFCourseEpisodesForParticipatedUsersMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        if user.is_authenticated:
            is_user_participated = PDFCourse.objects.filter(
                slug=slug, participated_users=user
            ).exists()

        else:
            is_user_participated = False

        if is_user_participated:
            return redirect(reverse("course:pdf_course_episodes", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class RedirectToVideoCourseEpisodesForParticipatedUsersMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        if user.is_authenticated:
            is_user_participated = VideoCourse.objects.filter(
                slug=slug, participated_users=user
            ).exists()

        else:
            is_user_participated = False

        if is_user_participated:
            return redirect(reverse("course:video_course_episodes", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)