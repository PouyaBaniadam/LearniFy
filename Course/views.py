import json

from django.contrib import messages
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import uri_to_iri
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View

from Account.mixins import AuthenticatedUsersOnlyMixin
from Account.models import FavoriteVideoCourse, Follow, CustomUser, Notification, FavoritePDFCourse
from Course.evaluations import exam_evaluations
from Financial.models import CartItem
from Course.filters import VideoCourseFilter, PDFCourseFilter
from Course.mixins import ParticipatedUsersPDFCoursesOnlyMixin, RedirectToPDFCourseEpisodesForParticipatedUsersMixin, \
    ParticipatedUsersVideoCoursesOnlyMixin, RedirectToVideoCourseEpisodesForParticipatedUsersMixin, \
    ParticipatedUsersPDFExamsOnlyMixin, InTimePDFExamsOnlyMixin, NoTimingPenaltyAllowedForPDFExamMixin, \
    ParticipatedUsersVideoExamsOnlyMixin, InTimeVideoExamsOnlyMixin, NoTimingPenaltyAllowedForVideoExamMixin
from Course.models import VideoCourse, VideoCourseComment, PDFCourse, PDFCourseComment, BoughtCourse, PDFCourseObject, \
    PDFCourseObjectDownloadedBy, VideoCourseObject, VideoCourseObjectDownloadedBy, PDFExam, PDFExamTempAnswer, \
    PDFExamDetail, PDFExamTimer, PDFExamResult, VideoExamResult, VideoExamTimer, VideoExam, VideoExamDetail, \
    VideoExamTempAnswer
from Home.mixins import URLStorageMixin
from Home.templatetags.filters import j_date_formatter, j_date_formatter_short


class AllVideoCourses(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'
    template_name = 'Course/all_video_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

        context['favorite_video_courses'] = favorite_video_courses

        return context

    def get_queryset(self):
        video_courses = VideoCourse.objects.select_related('category', 'teacher').order_by('-created_at')

        return video_courses


class VideoCourseDetail(RedirectToVideoCourseEpisodesForParticipatedUsersMixin, URLStorageMixin, DetailView):
    model = VideoCourse
    context_object_name = 'course'
    template_name = 'Course/video_course_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        is_follow_request_pending = False

        if user.is_authenticated:
            does_course_exists_in_cart = CartItem.objects.filter(
                cart__user=user, video_course=self.object, course_type="VID").exists()

            favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            does_course_exists_in_cart = False
            favorite_video_courses = []

        comments = self.object.video_course_comments.all()

        if self.request.user.is_authenticated:
            user_likes = VideoCourseComment.objects.filter(likes=user).values_list('id', flat=True)
            is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        else:
            user_likes = []
            is_following = False

        context['does_course_exists_in_cart'] = does_course_exists_in_cart
        context['favorite_video_courses'] = favorite_video_courses
        context['comments'] = comments
        context['user_likes'] = user_likes
        context['is_following'] = is_following
        context['is_follow_request_pending'] = is_follow_request_pending

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class VideoCourseByCategory(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'
    template_name = 'Course/video_courses_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        video_courses = get_list_or_404(VideoCourse, category__slug=slug)

        return video_courses


@method_decorator(csrf_exempt, name='dispatch')
class RegisterInVideoCourse(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('courseId')
        user = self.request.user

        video_course = VideoCourse.objects.get(id=course_id)
        if video_course.payment_type == "F":
            if not VideoCourse.objects.filter(id=course_id, participated_users=user).exists():
                video_course.participated_users.add(user)
                video_course.save()

                BoughtCourse.objects.create(user=user, video_course=video_course)

                return JsonResponse(data={"message": f"ثبت نام در دوره {video_course.name} با موفقیت انجام شد."},
                                    status=200)

            else:
                return JsonResponse(data={"message": f"شما قبلا در دوره {video_course.name} ثبت نام کردید."},
                                    status=400)


class VideoCourseFilterView(View):
    template_name = "Course/video_course_filter.html"

    def get(self, request):
        video_courses = VideoCourse.objects.all()
        video_course_filter = VideoCourseFilter(request.GET, queryset=video_courses)

        user = self.request.user

        favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

        context = {
            'video_courses': video_course_filter.qs,
            'favorite_video_courses': favorite_video_courses
        }

        return render(request=request, template_name=self.template_name, context=context)


@method_decorator(csrf_exempt, name='dispatch')
class ToggleVideoCourseFavorite(View):
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('id')
        user_id = request.POST.get('user')
        user = CustomUser.objects.get(username=user_id)

        try:
            video_course = VideoCourse.objects.get(id=course_id)
            if FavoriteVideoCourse.objects.filter(video_course=video_course, user=user).exists():
                FavoriteVideoCourse.objects.filter(video_course=video_course, user=user).delete()
                return JsonResponse({'success': True, 'action': 'removed'})
            else:
                FavoriteVideoCourse.objects.create(video_course=video_course, user=user)
                return JsonResponse({'success': True, 'action': 'added'})
        except VideoCourse.DoesNotExist:
            pass

        return JsonResponse({'success': False}, status=400)


class VideoCourseEpisodes(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoCoursesOnlyMixin, URLStorageMixin,
                          DetailView):
    model = VideoCourse
    context_object_name = 'course'
    template_name = 'Course/video_course_episodes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        is_follow_request_pending = False

        favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

        if user.is_authenticated:
            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        comments = self.object.video_course_comments.all()

        if self.request.user.is_authenticated:
            user_likes = VideoCourseComment.objects.filter(likes=user).values_list('id', flat=True)
            is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        else:
            user_likes = []
            is_following = False

        exams = VideoExam.objects.filter(video_course_season__course=self.object)

        context['favorite_video_courses'] = favorite_video_courses
        context['comments'] = comments
        context['user_likes'] = user_likes
        context['is_following'] = is_following
        context['is_follow_request_pending'] = is_follow_request_pending
        context['exams'] = exams

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class AddVideoCourseComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        slug = kwargs.get('slug')

        video_course = get_object_or_404(VideoCourse, slug=slug)

        VideoCourseComment.objects.create(user=user, text=text, video_course=video_course, parent_id=parent_id)
        messages.success(request, f"نظر شما با موفقیت ثبت شد.")

        fragment = 'reply_section'
        url = reverse('course:video_course_detail', kwargs={'slug': slug}) + f'#{fragment}'

        return redirect(url)


class DeleteVideoCourseComment(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        comment = VideoCourseComment.objects.get(id=id)
        video_course = VideoCourse.objects.get(video_course_comments=comment)
        comment.delete()

        messages.success(request, f"نظر شما با موفقیت حذف شد.")

        return redirect(reverse("course:video_course_detail", kwargs={'slug': video_course.slug}))


class LikeVideoCourseComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')

            comment = get_object_or_404(VideoCourseComment, id=comment_id)
            user = request.user

            if user in comment.likes.all():
                comment.likes.remove(user)
                liked = False
            else:
                comment.likes.add(user)
                liked = True

            return JsonResponse({'liked': liked})
        except VideoCourseComment.DoesNotExist:
            return JsonResponse({'error': 'چنین کامنتی یافت نشد.'}, status=404)


class AllPDFCourses(URLStorageMixin, ListView):
    model = PDFCourse
    context_object_name = 'pdf_courses'
    template_name = 'Course/all_pdf_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

        context['favorite_pdf_courses'] = favorite_pdf_courses

        return context

    def get_queryset(self):
        pdf_courses = PDFCourse.objects.select_related('category', 'teacher').order_by('-created_at')

        return pdf_courses


@method_decorator(csrf_exempt, name='dispatch')
class RegisterInPDFCourse(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('courseId')
        user = self.request.user

        pdf_course = PDFCourse.objects.get(id=course_id)
        if pdf_course.payment_type == "F":
            if not PDFCourse.objects.filter(id=course_id, participated_users=user).exists():
                pdf_course.participated_users.add(user)
                pdf_course.save()

                BoughtCourse.objects.create(user=user, pdf_course=pdf_course)

                return JsonResponse(data={"message": f"ثبت نام در دوره {pdf_course.name} با موفقیت انجام شد."},
                                    status=200)

            else:
                return JsonResponse(data={"message": f"شما قبلا در دوره {pdf_course.name} ثبت نام کردید."},
                                    status=400)


class PDFCourseFilterView(View):
    template_name = "Course/pdf_course_filter.html"

    def get(self, request):
        pdf_courses = PDFCourse.objects.all()
        pdf_course_filter = PDFCourseFilter(request.GET, queryset=pdf_courses)

        user = self.request.user
        favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

        context = {
            'pdf_courses': pdf_course_filter.qs,
            'favorite_pdf_courses': favorite_pdf_courses
        }

        return render(request=request, template_name=self.template_name, context=context)


class PDFCourseDetail(RedirectToPDFCourseEpisodesForParticipatedUsersMixin, URLStorageMixin, DetailView):
    model = PDFCourse
    context_object_name = 'course'
    template_name = 'Course/pdf_course_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        is_follow_request_pending = False

        favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

        if user.is_authenticated:
            does_course_exists_in_cart = CartItem.objects.filter(
                cart__user=user, pdf_course=self.object, course_type="PDF").exists()

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            does_course_exists_in_cart = False

        comments = self.object.pdf_course_comments.all()

        if self.request.user.is_authenticated:
            user_likes = PDFCourseComment.objects.filter(likes=user).values_list('id', flat=True)
            is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        else:
            user_likes = []
            is_following = False

        context['does_course_exists_in_cart'] = does_course_exists_in_cart
        context['favorite_pdf_courses'] = favorite_pdf_courses
        context['comments'] = comments
        context['user_likes'] = user_likes
        context['is_following'] = is_following
        context['is_follow_request_pending'] = is_follow_request_pending

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class PDFCourseByCategory(URLStorageMixin, ListView):
    model = PDFCourse
    context_object_name = 'pdf_courses'
    template_name = 'Course/pdf_courses_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        pdf_courses = get_list_or_404(PDFCourse, category__slug=slug)

        return pdf_courses


class AddPDFCourseComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        slug = kwargs.get('slug')

        pdf_course = get_object_or_404(PDFCourse, slug=slug)

        PDFCourseComment.objects.create(user=user, text=text, pdf_course=pdf_course, parent_id=parent_id)
        messages.success(request, f"نظر شما با موفقیت ثبت شد.")

        fragment = 'reply_section'
        url = reverse('course:pdf_course_detail', kwargs={'slug': slug}) + f'#{fragment}'

        return redirect(url)


class DeletePDFCourseComment(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        comment = PDFCourseComment.objects.get(id=id)
        pdf_course = PDFCourse.objects.get(pdf_course_comments=comment)
        comment.delete()

        messages.success(request, f"نظر شما با موفقیت حذف شد.")

        return redirect(reverse("course:pdf_course_detail", kwargs={'slug': pdf_course.slug}))


class LikePDFCourseComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')

            comment = get_object_or_404(PDFCourseComment, id=comment_id)
            user = request.user

            if user in comment.likes.all():
                comment.likes.remove(user)
                liked = False
            else:
                comment.likes.add(user)
                liked = True

            return JsonResponse({'liked': liked})
        except PDFCourseComment.DoesNotExist:
            return JsonResponse({'error': 'چنین کامنتی یافت نشد.'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class TogglePDFCourseFavorite(View):
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('id')
        user_id = request.POST.get('user')
        user = CustomUser.objects.get(username=user_id)

        try:
            pdf_course = PDFCourse.objects.get(id=course_id)
            if FavoritePDFCourse.objects.filter(pdf_course=pdf_course, user=user).exists():
                FavoritePDFCourse.objects.filter(pdf_course=pdf_course, user=user).delete()
                return JsonResponse({'success': True, 'action': 'removed'})
            else:
                FavoritePDFCourse.objects.create(pdf_course=pdf_course, user=user)
                return JsonResponse({'success': True, 'action': 'added'})
        except PDFCourse.DoesNotExist:
            pass

        return JsonResponse({'success': False}, status=400)


class PDFCourseEpisodes(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFCoursesOnlyMixin, URLStorageMixin, DetailView):
    model = PDFCourse
    context_object_name = 'course'
    template_name = 'Course/pdf_course_episodes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

        is_follow_request_pending = Notification.objects.filter(
            users=self.object.teacher,
            visibility="PV",
            following=self.object.teacher,
            follower=user,
            mode="S",
            type="FO",
        ).exists()

        comments = self.object.pdf_course_comments.all()

        user_likes = PDFCourseComment.objects.filter(likes=user).values_list('id', flat=True)
        is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        exams = PDFExam.objects.filter(pdf_course_season__course=self.object)

        context['favorite_pdf_courses'] = favorite_pdf_courses
        context['comments'] = comments
        context['user_likes'] = user_likes
        context['is_following'] = is_following
        context['is_follow_request_pending'] = is_follow_request_pending
        context['exams'] = exams

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


@method_decorator(csrf_exempt, name='dispatch')
class PDFCourseDownloadSession(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFCoursesOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.POST.get("course_id")
        pdf_course_object = PDFCourseObject.objects.get(id=course_id)

        pdf_file_path = pdf_course_object.pdf_file.path
        with open(pdf_file_path, 'rb') as f:
            download_file_name = f"{pdf_course_object.session} - {pdf_course_object.download_file_name}.pdf"
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{download_file_name}"'

            has_user_downloaded = PDFCourseObjectDownloadedBy.objects.filter(
                user=user
            ).exists()

            if not has_user_downloaded:
                PDFCourseObjectDownloadedBy.objects.create(
                    user=user, pdf_course_object=pdf_course_object
                )

            return response


@method_decorator(csrf_exempt, name='dispatch')
class VideoCourseDownloadSession(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoCoursesOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.POST.get("course_id")
        video_course_object = VideoCourseObject.objects.get(id=course_id)

        video_file_path = video_course_object.video_file.path
        with open(video_file_path, 'rb') as f:
            download_file_name = f"{video_course_object.session} - {video_course_object.download_file_name}.mp4"
            response = HttpResponse(f.read(), content_type='application/video')
            response['Content-Disposition'] = f'attachment; filename="{download_file_name}"'

            has_user_downloaded = VideoCourseObjectDownloadedBy.objects.filter(
                user=user
            ).exists()

            if not has_user_downloaded:
                VideoCourseObjectDownloadedBy.objects.create(
                    user=user, video_course_object=video_course_object
                )

            return response


class PDFExamDetailView(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFExamsOnlyMixin,
                        InTimePDFExamsOnlyMixin, URLStorageMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        pdf_exam = PDFExam.objects.get(slug=slug)

        try:
            pdf_exam_timer = PDFExamTimer.objects.get(user=user, pdf_exam=pdf_exam)
            ends_at = pdf_exam_timer.ends_at
            time_left = ends_at - timezone.now()

        except PDFExamTimer.DoesNotExist:
            ends_at = pdf_exam.duration + timezone.now()
            pdf_exam_timer = PDFExamTimer.objects.create(user=user, pdf_exam=pdf_exam, ends_at=ends_at)

            ends_at = pdf_exam_timer.ends_at
            time_left = ends_at - timezone.now()

        questions_and_answers = []

        pdf_exam_details = PDFExamDetail.objects.filter(pdf_exam__slug=slug)

        for pdf_exam_detail in pdf_exam_details:
            if PDFExamTempAnswer.objects.filter(
                    user=user,
                    question=pdf_exam_detail.question).exists():

                pdf_exam_temp_answer = PDFExamTempAnswer.objects.get(user=user,
                                                                     question=pdf_exam_detail.question
                                                                     )

                questions_and_answers.append(
                    {
                        "id": pdf_exam_detail.id,
                        "slug": pdf_exam_detail.pdf_exam.slug,
                        "question": pdf_exam_detail.question,
                        "answer_1": pdf_exam_detail.answer_1,
                        "answer_2": pdf_exam_detail.answer_2,
                        "answer_3": pdf_exam_detail.answer_3,
                        "answer_4": pdf_exam_detail.answer_4,
                        "selected_answer": pdf_exam_temp_answer.selected_answer
                    }
                )

            else:
                questions_and_answers.append(
                    {
                        "id": pdf_exam_detail.id,
                        "slug": pdf_exam_detail.pdf_exam.slug,
                        "question": pdf_exam_detail.question,
                        "answer_1": pdf_exam_detail.answer_1,
                        "answer_2": pdf_exam_detail.answer_2,
                        "answer_3": pdf_exam_detail.answer_3,
                        "answer_4": pdf_exam_detail.answer_4,
                        "selected_answer": None
                    }
                )

        context = {
            "pdf_exam_details": pdf_exam_details,
            "questions_and_answers": questions_and_answers,
            "time_left": int(time_left.total_seconds()),
            "slug": slug
        }

        return render(request=request, template_name="Course/pdf_exam_detail.html", context=context)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitPDFExamTempAnswer(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFExamsOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        question = request.POST.get("question")
        selected_answer = request.POST.get("selected_answer")

        pdf_exam_detail = PDFExamDetail.objects.filter(pdf_exam__slug=slug).last()

        try:
            pdf_exam_temp_answer = PDFExamTempAnswer.objects.get(user=user, question=question)

            if pdf_exam_temp_answer.selected_answer != selected_answer:
                pdf_exam_temp_answer.selected_answer = selected_answer
                pdf_exam_temp_answer.question = question
                pdf_exam_temp_answer.save()

                return JsonResponse(
                    data={
                        "message": "changed",
                        "id": pdf_exam_temp_answer.pdf_exam_detail.id
                    },
                    status=200
                )

            else:
                id = pdf_exam_temp_answer.pdf_exam_detail.id
                pdf_exam_temp_answer.delete()

                return JsonResponse(
                    data={
                        "message": "removed",
                        "id": id
                    },
                    status=200
                )

        except PDFExamTempAnswer.DoesNotExist:
            temp_answer = PDFExamTempAnswer.objects.create(
                user=user,
                pdf_exam_detail=pdf_exam_detail,
                question=question,
                selected_answer=selected_answer
            )

            return JsonResponse(
                data={
                    "message": "added",
                    "id": temp_answer.pdf_exam_detail.id
                },
                status=200
            )


class SubmitPDFExamFinalAnswer(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFExamsOnlyMixin,
                               NoTimingPenaltyAllowedForPDFExamMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        questions_and_answers = []

        pdf_exam_details = PDFExamDetail.objects.filter(pdf_exam__slug=slug)
        pdf_exam = PDFExam.objects.get(slug=slug)
        coefficient_number = pdf_exam.pdf_course_season.course.coefficient_number

        for pdf_exam_detail in pdf_exam_details:
            if PDFExamTempAnswer.objects.filter(
                    user=user,
                    question=pdf_exam_detail.question).exists():

                pdf_exam_temp_answer = PDFExamTempAnswer.objects.get(user=user,
                                                                     question=pdf_exam_detail.question
                                                                     )

                questions_and_answers.append(
                    {
                        "correct_answer": pdf_exam_detail.correct_answer,
                        "selected_answer": pdf_exam_temp_answer.selected_answer
                    }
                )

            else:
                questions_and_answers.append(
                    {
                        "correct_answer": pdf_exam_detail.correct_answer,
                        "selected_answer": None
                    }
                )
        exam_result = []

        for item in questions_and_answers:
            if item["selected_answer"] is None:
                exam_result.append(None)

            elif item["correct_answer"] == item["selected_answer"]:
                exam_result.append(True)

            else:
                exam_result.append(False)

        percentage, true_answers_count, false_answers_count, none_answers_count = exam_evaluations(
            answers=exam_result,
            coefficient_number=coefficient_number
        )

        pdf_exam_result = PDFExamResult.objects.create(
            user=user,
            pdf_exam=pdf_exam,
            percentage=percentage,
            true_answers_count=true_answers_count,
            false_answers_count=false_answers_count,
            none_answers_count=none_answers_count,
        )

        temp_answers = PDFExamTempAnswer.objects.filter(user=user)

        for temp_answer in temp_answers:
            temp_answer.delete()

        if pdf_exam_result.result_status == "E" or pdf_exam_result.result_status == "G":
            messages.success(request=request,
                             message=f"شما در آزمون {pdf_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        if pdf_exam_result.result_status == "N":
            messages.warning(request=request,
                             message=f"شما در آزمون {pdf_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        if pdf_exam_result.result_status == "B":
            messages.error(request=request,
                           message=f"شما در آزمون {pdf_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        course = pdf_exam.pdf_course_season.course

        pdf_exam_timer = PDFExamTimer.objects.get(user=user, pdf_exam=pdf_exam)
        pdf_exam_timer.ends_at = timezone.now()
        pdf_exam_timer.save()

        return redirect(reverse("course:pdf_course_episodes", kwargs={'slug': course.slug}))


class PDFExamResultView(AuthenticatedUsersOnlyMixin, ParticipatedUsersPDFExamsOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        pdf_exam_results = PDFExamResult.objects.filter(user=user, pdf_exam__slug=slug)

        exam_result = []

        for result in pdf_exam_results:
            exam_result.append(
                {
                    "percentage": f"{int(result.percentage)}%",
                    "result_status": result.result_status,
                    "created_at": j_date_formatter_short(result.created_at)
                }
            )

        return JsonResponse(
            data={
                "exam_result": exam_result,
            },
            status=200
        )


class VideoExamDetailView(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoExamsOnlyMixin,
                          InTimeVideoExamsOnlyMixin, URLStorageMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        video_exam = VideoExam.objects.get(slug=slug)

        try:
            video_exam_timer = VideoExamTimer.objects.get(user=user, video_exam=video_exam)
            ends_at = video_exam_timer.ends_at
            time_left = ends_at - timezone.now()

        except VideoExamTimer.DoesNotExist:
            ends_at = video_exam.duration + timezone.now()
            video_exam_timer = VideoExamTimer.objects.create(user=user, video_exam=video_exam, ends_at=ends_at)

            ends_at = video_exam_timer.ends_at
            time_left = ends_at - timezone.now()

        questions_and_answers = []

        video_exam_details = VideoExamDetail.objects.filter(video_exam__slug=slug)

        for video_exam_detail in video_exam_details:
            if VideoExamTempAnswer.objects.filter(
                    user=user,
                    question=video_exam_detail.question).exists():

                video_exam_temp_answer = VideoExamTempAnswer.objects.get(user=user,
                                                                         question=video_exam_detail.question
                                                                         )

                questions_and_answers.append(
                    {
                        "id": video_exam_detail.id,
                        "slug": video_exam_detail.video_exam.slug,
                        "question": video_exam_detail.question,
                        "answer_1": video_exam_detail.answer_1,
                        "answer_2": video_exam_detail.answer_2,
                        "answer_3": video_exam_detail.answer_3,
                        "answer_4": video_exam_detail.answer_4,
                        "selected_answer": video_exam_temp_answer.selected_answer
                    }
                )

            else:
                questions_and_answers.append(
                    {
                        "id": video_exam_detail.id,
                        "slug": video_exam_detail.video_exam.slug,
                        "question": video_exam_detail.question,
                        "answer_1": video_exam_detail.answer_1,
                        "answer_2": video_exam_detail.answer_2,
                        "answer_3": video_exam_detail.answer_3,
                        "answer_4": video_exam_detail.answer_4,
                        "selected_answer": None
                    }
                )

        context = {
            "video_exam_details": video_exam_details,
            "questions_and_answers": questions_and_answers,
            "time_left": int(time_left.total_seconds()),
            "slug": slug
        }

        return render(request=request, template_name="Course/video_exam_detail.html", context=context)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitVideoExamTempAnswer(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoExamsOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        question = request.POST.get("question")
        selected_answer = request.POST.get("selected_answer")

        video_exam_detail = VideoExamDetail.objects.filter(video_exam__slug=slug).last()

        try:
            video_exam_temp_answer = VideoExamTempAnswer.objects.get(user=user, question=question)

            if video_exam_temp_answer.selected_answer != selected_answer:
                video_exam_temp_answer.selected_answer = selected_answer
                video_exam_temp_answer.question = question
                video_exam_temp_answer.save()

                return JsonResponse(
                    data={
                        "message": "changed"
                    },
                    status=200
                )

            else:
                video_exam_temp_answer.delete()

                return JsonResponse(
                    data={
                        "message": "removed"
                    },
                    status=200
                )

        except VideoExamTempAnswer.DoesNotExist:
            VideoExamTempAnswer.objects.create(
                user=user,
                video_exam_detail=video_exam_detail,
                question=question,
                selected_answer=selected_answer
            )

            return JsonResponse(
                data={
                    "message": "added"
                },
                status=200
            )


class SubmitVideoExamFinalAnswer(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoExamsOnlyMixin,
                                 NoTimingPenaltyAllowedForVideoExamMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        questions_and_answers = []

        video_exam_details = VideoExamDetail.objects.filter(video_exam__slug=slug)
        video_exam = VideoExam.objects.get(slug=slug)
        coefficient_number = video_exam.video_course_season.course.coefficient_number

        for video_exam_detail in video_exam_details:
            if VideoExamTempAnswer.objects.filter(
                    user=user,
                    question=video_exam_detail.question).exists():

                video_exam_temp_answer = VideoExamTempAnswer.objects.get(user=user,
                                                                         question=video_exam_detail.question
                                                                         )

                questions_and_answers.append(
                    {
                        "correct_answer": video_exam_detail.correct_answer,
                        "selected_answer": video_exam_temp_answer.selected_answer
                    }
                )

            else:
                questions_and_answers.append(
                    {
                        "correct_answer": video_exam_detail.correct_answer,
                        "selected_answer": None
                    }
                )
        exam_result = []

        for item in questions_and_answers:
            if item["selected_answer"] is None:
                exam_result.append(None)

            elif item["correct_answer"] == item["selected_answer"]:
                exam_result.append(True)

            else:
                exam_result.append(False)

        percentage, true_answers_count, false_answers_count, none_answers_count = exam_evaluations(
            answers=exam_result,
            coefficient_number=coefficient_number
        )

        video_exam_result = VideoExamResult.objects.create(
            user=user,
            video_exam=video_exam,
            percentage=percentage,
            true_answers_count=true_answers_count,
            false_answers_count=false_answers_count,
            none_answers_count=none_answers_count,
        )

        temp_answers = VideoExamTempAnswer.objects.filter(user=user)

        for temp_answer in temp_answers:
            temp_answer.delete()

        if video_exam_result.result_status == "E" or video_exam_result.result_status == "G":
            messages.success(request=request,
                             message=f"شما در آزمون {video_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        if video_exam_result.result_status == "N":
            messages.warning(request=request,
                             message=f"شما در آزمون {video_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        if video_exam_result.result_status == "B":
            messages.error(request=request,
                           message=f"شما در آزمون {video_exam.name}، مقدار {int(percentage)}% را کسب کردید!")

        course = video_exam.video_course_season.course

        video_exam_timer = VideoExamTimer.objects.get(user=user, video_exam=video_exam)
        video_exam_timer.ends_at = timezone.now()
        video_exam_timer.save()

        return redirect(reverse("course:video_course_episodes", kwargs={'slug': course.slug}))


class VideoExamResultView(AuthenticatedUsersOnlyMixin, ParticipatedUsersVideoExamsOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        video_exam_results = VideoExamResult.objects.filter(user=user, video_exam__slug=slug)

        exam_result = []

        for result in video_exam_results:
            exam_result.append(
                {
                    "percentage": f"{int(result.percentage)}%",
                    "result_status": result.result_status,
                    "created_at": j_date_formatter_short(result.created_at)
                }
            )

        return JsonResponse(
            data={
                "exam_result": exam_result,
            },
            status=200
        )
