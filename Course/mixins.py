from datetime import datetime

import pytz
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from Account.models import CustomUser
from Course.models import Exam, EnteredExamUser, UserFinalAnswer, PDFCourse, VideoCourse
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


class CheckForExamTimeMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        exam = Exam.objects.get(slug=slug)
        if EnteredExamUser.objects.filter(exam=exam, user=user).exists():
            entered_exam_user = EnteredExamUser.objects.get(exam=exam, user=user)

            date_1 = entered_exam_user.created_at
            date_2 = datetime.now(pytz.timezone('Iran'))

            total_duration = exam.total_duration.total_seconds()
            difference = get_time_difference(date_1=date_1, date_2=date_2)

            time_left = int(total_duration - difference)

            if time_left < 0:
                messages.error(request, f"متاسفانه زمان شما به اتمام رسیده و امکان شرکت در آزمون برای شما فراهم نیست.")

                return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class AllowedExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        exam = Exam.objects.get(slug=slug)

        if not exam.is_entrance_allowed:
            messages.error(request, f"با عرض پوزش، در حال حاضر شرکت در آزمون {exam.name} امکان پذیر نیست.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class AllowedFilesDownloadMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')

        exam = Exam.objects.get(slug=slug)

        if not exam.is_downloading_question_files_allowed:
            messages.error(request, f"متاسفانه امکان دانلود فایل آزمون {exam.name} فراهم نیست.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class NonFinishedExamsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user
        exam = Exam.objects.get(slug=slug)

        if UserFinalAnswer.objects.filter(user=user, exam=exam).exists():
            messages.error(request, f"شما قبلا پاسخنامه آزمون {exam.name} را ثبت کرده اید!")

            return redirect(reverse('course:exam_detail', kwargs={'slug': slug}))

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