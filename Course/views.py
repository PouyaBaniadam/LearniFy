import json
from datetime import datetime

import pytz
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import uri_to_iri
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View

from Account.mixins import AuthenticatedUsersOnlyMixin
from Account.models import FavoriteVideoCourse, Follow, CustomUser, Notification, FavoritePDFCourse
from Financial.models import CartItem
from Course.filters import VideoCourseFilter, PDFCourseFilter
from Course.mixins import CheckForExamTimeMixin, AllowedExamsOnlyMixin, \
    NonFinishedExamsOnlyMixin, ParticipatedUsersPDFCoursesOnlyMixin, \
    RedirectToPDFCourseEpisodesForParticipatedUsersMixin, ParticipatedUsersVideoCoursesOnlyMixin, \
    RedirectToVideoCourseEpisodesForParticipatedUsersMixin
from Course.models import VideoCourse, Exam, ExamAnswer, EnteredExamUser, UserFinalAnswer, VideoCourseComment, \
    PDFCourse, PDFCourseComment, BoughtCourse, PDFCourseObject, PDFCourseObjectDownloadedBy, VideoCourseObject, \
    VideoCourseObjectDownloadedBy
from Home.mixins import URLStorageMixin
from utils.useful_functions import get_time_difference


class AllVideoCourses(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'
    template_name = 'Course/all_video_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id',
                                                                                                            flat=True)
        else:
            favorite_video_courses = []

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

            favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id',
                                                                                                            flat=True)

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                title="درخواست فالو",
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


class AllBookCourses(URLStorageMixin, ListView):
    pass


class ExamDetail(URLStorageMixin, DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'Course/exam_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'designer')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        sections = ExamAnswer.objects.filter(exam=self.object)

        section_names = list(set(sections.values_list('section__name', flat=True)))

        #  Checks if user can enter exam anymore or not. (Based on entrance time)
        is_time_up = False

        if self.request.user.is_authenticated:
            if EnteredExamUser.objects.filter(
                    user=user, exam=self.object
            ).exists():
                entered_exam_user = EnteredExamUser.objects.get(user=user, exam=self.object)

                date_1 = entered_exam_user.created_at
                date_2 = datetime.now(pytz.timezone('Iran'))

                total_duration = self.object.total_duration.total_seconds()

                difference = get_time_difference(date_1=date_1, date_2=date_2)

                time_left = int(total_duration - difference)

                if time_left < 0:
                    is_time_up = True

            can_be_continued = False
            if EnteredExamUser.objects.filter(user=user, exam=self.object).exists():
                can_be_continued = True

            has_finished_exam = False
            if UserFinalAnswer.objects.filter(user=user, exam=self.object).exists():
                has_finished_exam = True

            try:
                is_user_registered = Exam.objects.filter(participated_users=user, slug=self.object.slug).exists()

            except TypeError:
                is_user_registered = False

        else:
            is_user_registered = False
            can_be_continued = False
            has_finished_exam = False

        context['is_time_up'] = is_time_up  # Returns a boolean
        context['is_user_registered'] = is_user_registered  # Returns a boolean
        context['can_be_continued'] = can_be_continued  # Returns a boolean
        context['has_finished_exam'] = has_finished_exam  # Returns a boolean
        context['sections_names'] = section_names  # Returns a list

        return context


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


class EnterExam(AuthenticatedUsersOnlyMixin, AllowedExamsOnlyMixin, CheckForExamTimeMixin, NonFinishedExamsOnlyMixin,
                URLStorageMixin, View):
    template_name = "Course/multiple_choice_exam.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')

        exam = Exam.objects.get(slug=slug)

        if not EnteredExamUser.objects.filter(exam=exam, user=user).exists():
            EnteredExamUser.objects.create(exam=exam, user=user)

        entered_exam_user = EnteredExamUser.objects.get(exam=exam, user=user)

        date_1 = entered_exam_user.created_at
        date_2 = datetime.now(pytz.timezone('Iran'))

        total_duration = exam.total_duration.total_seconds()

        difference = get_time_difference(date_1=date_1, date_2=date_2)

        time_left = int(total_duration - difference)

        answers = ExamAnswer.objects.values(
            "choice_1", "choice_2",
            "choice_3", "choice_4"
        )

        context = {
            'time_left': time_left,
            'answers': answers,
            'slug': exam.slug
        }

        return render(request=request, template_name=self.template_name, context=context)


class FinalExamSubmit(AuthenticatedUsersOnlyMixin, AllowedExamsOnlyMixin,
                      CheckForExamTimeMixin, NonFinishedExamsOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        exam_slug = self.kwargs['slug']
        exam = get_object_or_404(Exam, slug=exam_slug)

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_number = int(key.replace('question_', ''))
                selected_answer = value

                exam_answer = ExamAnswer.objects.get(exam=exam, question_number=question_number)
                if exam_answer.choice_1 == selected_answer:
                    UserFinalAnswer.objects.create(
                        user=user,
                        exam=exam,
                        question_number=question_number,
                        selected_answer=1
                    )

                if exam_answer.choice_2 == selected_answer:
                    UserFinalAnswer.objects.create(
                        user=user,
                        exam=exam,
                        question_number=question_number,
                        selected_answer=2
                    )

                if exam_answer.choice_3 == selected_answer:
                    UserFinalAnswer.objects.create(
                        user=user,
                        exam=exam,
                        question_number=question_number,
                        selected_answer=3
                    )

                if exam_answer.choice_4 == selected_answer:
                    UserFinalAnswer.objects.create(
                        user=user,
                        exam=exam,
                        question_number=question_number,
                        selected_answer=4
                    )

        messages.success(request, f"پاسخنامه آزمون {exam.name} با موقیت ثبت شد.")

        return redirect(reverse("course:exam_detail", kwargs={"slug": exam_slug}))


class CalculateExamResult(AuthenticatedUsersOnlyMixin, AllowedExamsOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user
        exam = get_object_or_404(Exam, slug=slug)

        context = {

        }

        return render(request, "Course/answer_results.html", context=context)


class VideoCourseFilterView(View):
    template_name = "Course/video_course_filter.html"

    def get(self, request):
        video_courses = VideoCourse.objects.all()
        video_course_filter = VideoCourseFilter(request.GET, queryset=video_courses)

        user = self.request.user
        if user.is_authenticated:
            favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id',
                                                                                                            flat=True)
        else:
            favorite_video_courses = []

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
        except Exam.DoesNotExist:
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

        if user.is_authenticated:
            favorite_video_courses = VideoCourse.objects.filter(favoritevideocourse__user=user).values_list('id',
                                                                                                            flat=True)

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                title="درخواست فالو",
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            favorite_video_courses = []

        comments = self.object.video_course_comments.all()

        if self.request.user.is_authenticated:
            user_likes = VideoCourseComment.objects.filter(likes=user).values_list('id', flat=True)
            is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        else:
            user_likes = []
            is_following = False

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
        if user.is_authenticated:
            favorite_pdf_courses = PDFCourse.objects.filter(favoritepdfcourse__user=user).values_list('id',
                                                                                                      flat=True)
        else:
            favorite_pdf_courses = []

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
        if user.is_authenticated:
            favorite_pdf_courses = PDFCourse.objects.filter(favoritepdfcourse__user=user).values_list('id',
                                                                                                      flat=True)
        else:
            favorite_pdf_courses = []

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

        if user.is_authenticated:
            does_course_exists_in_cart = CartItem.objects.filter(
                cart__user=user, pdf_course=self.object, course_type="PDF").exists()

            favorite_pdf_courses = PDFCourse.objects.filter(favoritepdfcourse__user=user).values_list('id',
                                                                                                      flat=True)

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                title="درخواست فالو",
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            does_course_exists_in_cart = False
            favorite_pdf_courses = []

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
        except Exam.DoesNotExist:
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

        is_follow_request_pending = False

        if user.is_authenticated:
            favorite_pdf_courses = PDFCourse.objects.filter(favoritepdfcourse__user=user).values_list('id',
                                                                                                      flat=True)

            is_follow_request_pending = Notification.objects.filter(
                users=self.object.teacher,
                title="درخواست فالو",
                visibility="PV",
                following=self.object.teacher,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            favorite_pdf_courses = []

        comments = self.object.pdf_course_comments.all()

        if self.request.user.is_authenticated:
            user_likes = PDFCourseComment.objects.filter(likes=user).values_list('id', flat=True)
            is_following = Follow.objects.filter(follower=user, following=self.object.teacher).exists()

        else:
            user_likes = []
            is_following = False

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
