from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import Notification, Wallet, CustomUser
from Course.models import PDFCourseObjectDownloadedBy, VideoCourseObjectDownloadedBy, PDFExamResult, VideoExamResult
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
            message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{stars} امتیاز</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> به امتیازات خود اضافه کردید.</span></p>',
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
            message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">شما </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{stars} امتیاز</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> به امتیازات خود اضافه کردید.</span></p>',
            visibility="PV",
            mode="S",
            type="AN",
        )

        notification.users.add(user)
        notification.save()


@receiver(post_save, sender=BoughtCourse)
def charge_teacher_wallet(instance, created, **kwargs):
    if created:
        how_much_to_pay_to_teacher = instance.cost - (5 / 100 * instance.cost)
        humanized_how_much_to_pay_to_teacher = "{:,}".format(int(how_much_to_pay_to_teacher))

        if instance.pdf_course:
            teacher = instance.pdf_course.teacher

            notification = Notification.objects.create(
                title="ثبت نام دوره",
                message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">کاربر </span><span style="color:hsl(240,75%,60%);">{instance.user.username}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> در دوره </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{instance.pdf_course.name}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> ثبت نام کرد و مبلغ </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{humanized_how_much_to_pay_to_teacher}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> تومان به کیف پول شما واریز شد.</span></p>',
                visibility="PV",
                mode="S",
                type="AN",
            )

            notification.users.add(teacher)
            notification.save()

        if instance.video_course:
            teacher = instance.video_course.teacher

            notification = Notification.objects.create(
                title="ثبت نام دوره",
                message=f'<p><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);">کاربر </span><span style="color:hsl(240,75%,60%);">{instance.user.username}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> در دوره </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{instance.video_course.name}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> ثبت نام کرد و مبلغ </span><span style="background-color:rgb(255,255,255);color:hsl(240,75%,60%);">{humanized_how_much_to_pay_to_teacher}</span><span style="background-color:rgb(255,255,255);color:rgb(75,85,99);"> تومان به کیف پول شما واریز شد.</span></p>',
                visibility="PV",
                mode="S",
                type="AN",
            )

            notification.users.add(teacher)
            notification.save()

        wallet = Wallet.objects.get(user=teacher)
        wallet.charge_wallet(how_much_to_pay_to_teacher)
        wallet.save()


@receiver(post_save, sender=PDFExamResult)
def add_to_user_stars_after_pdf_exam(instance, created, **kwargs):
    if created:
        pdf_exam_taken_part_count = PDFExamResult.objects.filter(
            user=instance.user,
            pdf_exam=instance.pdf_exam
        ).count()

        if pdf_exam_taken_part_count <= 1:
            coefficient_number = instance.pdf_exam.pdf_course_season.course.coefficient_number

            if instance.result_status == "E":
                stars = coefficient_number * 30

            if instance.result_status == "G":
                stars = coefficient_number * 20

            if instance.result_status == "N":
                stars = coefficient_number * 10

            if instance.result_status == "B":
                stars = coefficient_number

            user = CustomUser.objects.get(username=instance.user.username)
            user.stars += stars
            user.save()


@receiver(post_save, sender=VideoExamResult)
def add_to_user_stars_after_video_exam(instance, created, **kwargs):
    if created:
        video_exam_taken_part_count = VideoExamResult.objects.filter(
            user=instance.user,
            video_exam=instance.video_exam
        ).count()

        if video_exam_taken_part_count <= 1:
            coefficient_number = instance.video_exam.video_course_season.course.coefficient_number

            if instance.result_status == "E":
                stars = coefficient_number * 30

            if instance.result_status == "G":
                stars = coefficient_number * 20

            if instance.result_status == "N":
                stars = coefficient_number * 10

            if instance.result_status == "B":
                stars = coefficient_number

            user = CustomUser.objects.get(username=instance.user.username)
            user.stars += stars
            user.save()
