from datetime import datetime

import pytz
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from Account.models import CustomUser
from Course.models import Exam, EnteredExamUser, DownloadedQuestionFile, UserFinalAnswer
from utils.useful_functions import get_time_difference


class ParticipatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        user = CustomUser.objects.get(username=user.username)
        can_user_participate = Exam.objects.filter(slug=slug, participated_users=user).exists()

        if not can_user_participate:
            redirect_url = request.session.get('current_url')

            messages.error(request, f"ابتدا در آزمون ثبت نام کنید!")

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)


class CheckForExamTimeMixin:
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


class AllowedExamsOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        exam = Exam.objects.get(slug=slug)

        if not exam.is_entrance_allowed:
            messages.error(request, f"با عرض پوزش، در حال حاضر شرکت در آزمون {exam.name} امکان پذیر نیست.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class DownloadedQuestionsFileFirstMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        if not DownloadedQuestionFile.objects.filter(exam__slug=slug, user=user).exists():
            messages.error(request, f"جهت ورود به آزمون، ابتدا باید فایل سوالات را دانلود کنید.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class AllowedFilesDownloadMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')

        exam = Exam.objects.get(slug=slug)

        if not exam.is_downloading_question_files_allowed:
            messages.error(request, f"متاسفانه امکان دانلود فایل آزمون {exam.name} فراهم نیست.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class NonFinishedExamsOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user
        exam = Exam.objects.get(slug=slug)

        if UserFinalAnswer.objects.filter(user=user, exam=exam).exists():
            messages.error(request, f"شما قبلا پاسخنامه آزمون {exam.name} را ثبت کرده اید!")

            return redirect(reverse('course:exam_detail', kwargs={'slug': slug}))

        return super().dispatch(request, *args, **kwargs)
