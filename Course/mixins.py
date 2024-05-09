from datetime import datetime, timedelta

import pytz
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View

from Account.models import CustomUser
from Course.models import PDFCourse, VideoCourse, PDFExam, PDFExamTimer, VideoExam, VideoExamTimer
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


class ParticipatedUsersPDFExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        pdf_exam = PDFExam.objects.get(slug=slug)

        if user != pdf_exam.pdf_course_season.course.teacher:
            can_user_participate = PDFExam.objects.filter(
                slug=slug,
                pdf_course_season__course__participated_users=user
            ).exists()

            if not can_user_participate:
                redirect_url = request.session.get('current_url')

                messages.error(request, f"شما مجوز دسترسی به این صفحه را ندارید!")

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)


class ParticipatedUsersVideoExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        video_exam = VideoExam.objects.get(slug=slug)

        if user != video_exam.video_course_season.course.teacher:
            can_user_participate = VideoExam.objects.filter(
                slug=slug,
                video_course_season__course__participated_users=user
            ).exists()

            if not can_user_participate:
                redirect_url = request.session.get('current_url')

                messages.error(request, f"شما مجوز دسترسی به این صفحه را ندارید!")

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


class InTimePDFExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")
        pdf_exam = PDFExam.objects.get(slug=slug)
        course = pdf_exam.pdf_course_season.course

        try:
            pdf_exam_timer = PDFExamTimer.objects.get(user=user, pdf_exam=pdf_exam)
            ends_at = pdf_exam_timer.ends_at
            time_difference = ends_at - timezone.now()

            if time_difference.total_seconds() <= -86400:
                pdf_exam_timer.delete()

            if -86400 < time_difference.total_seconds() < 0:
                time_difference = timedelta(seconds=-(-86400 - time_difference.total_seconds()))

                hours = abs(time_difference.days) * 24 + time_difference.seconds // 3600
                minutes = (time_difference.seconds % 3600) // 60

                humanized_time = f"{hours} ساعت و {minutes} دقیقه "

                messages.error(request,
                               f" زمان این آزمون به اتمام رسیده و امکان ورود به آن تا {humanized_time} دیگر وجود ندارد. ")
                return redirect(reverse("course:pdf_course_episodes", kwargs={"slug": course.slug}))

        except PDFExamTimer.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class NoTimingPenaltyAllowedForPDFExamMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")
        pdf_exam = PDFExam.objects.get(slug=slug)

        pdf_exam_timer = PDFExamTimer.objects.get(user=user, pdf_exam=pdf_exam)
        ends_at = pdf_exam_timer.ends_at
        time_left = ends_at - timezone.now()

        if time_left.total_seconds() < -60:
            messages.error(request=request,
                           message=f"""
این آزمون مورد قبول نیست!
زمان این آژمون بیش از 1 دقیقه پیش به اتمام رسیده و احتمالا خطایی توسط شما رخ داده!
"""
                           )

            course = pdf_exam.pdf_course_season.course

            return redirect(reverse("course:pdf_course_episodes", kwargs={"slug": course.slug}))

        return super().dispatch(request, *args, **kwargs)


class InTimeVideoExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")
        video_exam = VideoExam.objects.get(slug=slug)
        course = video_exam.video_course_season.course

        try:
            video_exam_timer = VideoExamTimer.objects.get(user=user, video_exam=video_exam)
            ends_at = video_exam_timer.ends_at
            time_difference = ends_at - timezone.now()

            if time_difference.total_seconds() <= -86400:
                video_exam_timer.delete()

            if -86400 < time_difference.total_seconds() < 0:
                time_difference = timedelta(seconds=-(-86400 - time_difference.total_seconds()))

                hours = abs(time_difference.days) * 24 + time_difference.seconds // 3600
                minutes = (time_difference.seconds % 3600) // 60

                humanized_time = f"{hours} ساعت و {minutes} دقیقه "

                messages.error(request,
                               f" زمان این آزمون به اتمام رسیده و امکان ورود به آن تا {humanized_time} دیگر وجود ندارد. ")
                return redirect(reverse("course:video_course_episodes", kwargs={"slug": course.slug}))

        except VideoExamTimer.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class NoTimingPenaltyAllowedForVideoExamMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")
        video_exam = VideoExam.objects.get(slug=slug)

        video_exam_timer = VideoExamTimer.objects.get(user=user, video_exam=video_exam)
        ends_at = video_exam_timer.ends_at
        time_left = ends_at - timezone.now()

        if time_left.total_seconds() < -60:
            messages.error(request=request,
                           message=f"""
این آزمون مورد قبول نیست!
زمان این آژمون بیش از 1 دقیقه پیش به اتمام رسیده و احتمالا خطایی توسط شما رخ داده!
"""
                           )

            course = video_exam.video_course_season.course

            return redirect(reverse("course:video_course_episodes", kwargs={"slug": course.slug}))

        return super().dispatch(request, *args, **kwargs)
