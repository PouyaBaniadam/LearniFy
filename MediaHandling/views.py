import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import redirect

from Course.models import PDFCourseObject, VideoCourseObject


def serve_protected_media(request, filepath):
    user = request.user

    if "Course/PDFCourse/tutorials" in filepath:
        pdf_course_object = PDFCourseObject.objects.get(pdf_file=filepath)

        has_user_participated_in_pdf_course = (user in pdf_course_object.pdf_course.participated_users.all() and
                                               user != pdf_course_object.pdf_course.teacher)

        if has_user_participated_in_pdf_course:
            if user.is_authenticated:
                if not has_user_participated_in_pdf_course:
                    messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                    redirect_url = request.session.get('current_url')

                    if redirect_url is not None:
                        return redirect(redirect_url)

                    return redirect("home:home")

            else:
                messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                redirect_url = request.session.get('current_url')

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

    if "Course/VideoCourse/tutorials" in filepath:
        video_course_object = VideoCourseObject.objects.get(video_file=filepath)

        has_user_participated_in_video_course = (user in video_course_object.video_course.participated_users.all() and
                                                 user != video_course_object.video_course.teacher)

        if has_user_participated_in_video_course:
            if user.is_authenticated:
                if not has_user_participated_in_video_course:
                    messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                    redirect_url = request.session.get('current_url')

                    if redirect_url is not None:
                        return redirect(redirect_url)

                    return redirect("home:home")

            else:
                messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                redirect_url = request.session.get('current_url')

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

    full_filepath = os.path.join(settings.MEDIA_ROOT, filepath)

    if not os.path.exists(full_filepath):
        messages.error(request, f"چنین فایلی یافت نشد!")

        redirect_url = request.session.get('current_url')

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")

    return FileResponse(open(full_filepath, 'rb'))
