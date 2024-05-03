from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import Notification
from Course.models import PDFCourseObjectDownloadedBy, VideoCourseObjectDownloadedBy
from Financial.models import BoughtCourse


@receiver(post_save, sender=BoughtCourse)
def create_register_in_course_notification(instance, created, **kwargs):
    if created:
        user = instance.user
        # ToDo: change hostname later.

        if instance.pdf_course:
            notification = Notification.objects.create(
                title="ثبت نام دوره",
                message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما در دوره </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{instance.pdf_course.name}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> ثبت نام کردید.</span></p>',
                visibility="PV",
                mode="S",
                type="AN",
            )
            notification.users.add(user)
            notification.save()

        if instance.video_course:
            notification = Notification.objects.create(
                title="ثبت نام دوره",
                message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما در دوره </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{instance.video_course.name}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> ثبت نام کردید.</span></p>',
                visibility="PV",
                mode="S",
                type="AN",
            )
            notification.users.add(user)
            notification.save()


@receiver(post_save, sender=PDFCourseObjectDownloadedBy)
def add_to_user_stars_for_downloading_pdf_course_object(instance, created, **kwargs):
    if created:
        user = instance.user

        coefficient_number = instance.pdf_course_object.pdf_course.coefficient_number
        stars = coefficient_number * 10

        user.stars += stars
        user.save()

        notification = Notification.objects.create(
            title="کسب امتیاز",
            message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{stars}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> به امتیازات خود اضافه کردید.</span></p>',
            visibility="PV",
            mode="S",
            type="AN",
        )

        notification.users.add(user)
        notification.save()


@receiver(post_save, sender=VideoCourseObjectDownloadedBy)
def add_to_user_stars_for_downloading_video_course_object(instance, created, **kwargs):
    if created:
        user = instance.user

        coefficient_number = instance.video_course_object.video_course.coefficient_number
        stars = coefficient_number * 10

        user.stars += stars
        user.save()

        notification = Notification.objects.create(
            title="کسب امتیاز",
            message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{stars}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> به امتیازات خود اضافه کردید.</span></p>',
            visibility="PV",
            mode="S",
            type="AN",
        )

        notification.users.add(user)
        notification.save()
