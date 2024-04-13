import random
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, ListView, DetailView

from Account.forms import OTPRegisterForm, CheckOTPForm, RegularLogin, ForgetPasswordForm, ChangePasswordForm
from Account.mixins import NonAuthenticatedUsersOnlyMixin, AuthenticatedUsersOnlyMixin, OwnerRequiredMixin
from Account.models import CustomUser, OTP, Notification, Wallet, NewsLetter, Follow, FavoriteExam
from Course.models import Exam
from Home.mixins import URLStorageMixin


class RegisterView(NonAuthenticatedUsersOnlyMixin, FormView):
    template_name = "Account/register.html"
    form_class = OTPRegisterForm

    def form_valid(self, form):
        sms_code = random.randint(a=1000, b=9999)
        mobile_phone = form.cleaned_data.get('mobile_phone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        uuid = str(uuid4())

        OTP.objects.create(mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid, username=username,
                           password=password, otp_type="R")

        # send_register_sms(receptor=mobile_phone, sms_code=sms_code)
        print(sms_code)

        return redirect(reverse("account:check_otp") + f"?uuid={uuid}&mobile_phone={mobile_phone}")

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogInView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = RegularLogin
    template_name = 'Account/login.html'

    def form_valid(self, form):
        request = self.request
        mobile_phone_or_username = form.cleaned_data.get('mobile_phone_or_username')
        password = form.cleaned_data.get('password')

        if mobile_phone_or_username.isdigit():
            user = CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

        else:
            user = CustomUser.objects.get(username=mobile_phone_or_username)

        username = user.username

        authenticated_user = authenticate(request=request, username=username, password=password)

        if authenticated_user is not None:
            login(request=request, user=user)

        else:
            form.add_error(field="mobile_phone_or_username", error="هیچ حساب کاربری با این مشخصات یافت نشد.")

            return self.form_invalid(form)

        redirect_url = request.session.get('current_url')

        if redirect_url is not None:
            messages.success(request, f"{user.username} عزیز، خوش آمدید.")

            return redirect(redirect_url)

        return redirect(reverse("account:owner_profile", kwargs={"slug": request.user.username}))

    def get_success_url(self):
        referring_url = self.request.session.pop(key="referring_url", default=None)
        return referring_url or reverse_lazy("account:owner_profile")


class LogOutView(AuthenticatedUsersOnlyMixin, View):
    def get(self, request):
        redirect_url = request.session.pop('current_url')

        logout(request=request)

        messages.success(request, f"شما با موفقیت از حساب کاربری خود خارج شدید.")

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")


class ChangePasswordView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = ChangePasswordForm
    template_name = 'Account/change_password.html'

    def form_valid(self, form):
        request = self.request
        new_password = form.cleaned_data.get('password')
        uuid = request.GET.get('uuid')

        otp = OTP.objects.get(uuid=uuid)
        mobile_phone = otp.mobile_phone

        user = CustomUser.objects.get(mobile_phone=mobile_phone)

        user.set_password(raw_password=new_password)
        user.save()

        login(request=request, user=user)

        otp.delete()

        redirect_url = request.session.get('current_url')

        messages.success(request, f"رمز عبور شما با موفقیت تغییر یافت.")

        if redirect_url is not None:
            return redirect(redirect_url)

        else:
            return redirect(reverse('account:owner_profile', kwargs={'slug': self.request.user.username}))

    def form_invalid(self, form):
        return super().form_invalid(form)


class ForgetPasswordView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = ForgetPasswordForm
    template_name = "Account/forget_password.html"

    def form_valid(self, form):
        mobile_phone_or_username = form.cleaned_data.get('mobile_phone_or_username')

        if str(mobile_phone_or_username).isdigit():
            user = CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

        else:
            user = CustomUser.objects.get(username=mobile_phone_or_username)

        mobile_phone = user.mobile_phone
        username = user.username

        sms_code = random.randint(a=1000, b=9999)
        uuid = str(uuid4())

        OTP.objects.create(username=username, mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid,
                           otp_type="F")

        # send_forget_password_sms(receptor=mobile_phone, sms_code=sms_code)
        print(sms_code)

        return redirect(reverse(viewname="account:check_otp") + f"?uuid={uuid}&mobile_phone={mobile_phone}")

    def form_invalid(self, form):
        return super().form_invalid(form)


class CheckOTPView(FormView):
    form_class = CheckOTPForm
    template_name = 'Account/check_otp.html'

    def form_valid(self, form):
        request = self.request
        uuid = request.GET.get('uuid')
        sms_code = form.cleaned_data.get('sms_code')

        if OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="R").exists():
            otp = OTP.objects.get(uuid=uuid)

            mobile_phone = otp.mobile_phone
            username = otp.username
            password = otp.password

            user = CustomUser.objects.create_user(mobile_phone=mobile_phone, username=username)
            Wallet.objects.create(owner=user)

            user.set_password(password)
            user.save()

            login(request=request, user=user)

            otp = OTP.objects.get(uuid=uuid)
            otp.delete()

            messages.success(request, f"{user.username} عزیز، حساب کاربری شما با موفقیت ایجاد شد.")

            return redirect(reverse("account:owner_profile", kwargs={"slug": user.username}))

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="F").exists():
            return redirect(reverse(viewname="account:change_password") + f"?uuid={uuid}")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="D").exists():
            otp = OTP.objects.get(uuid=uuid)
            username = otp.username

            user_to_be_deleted = CustomUser.objects.get(username=username)

            user_to_be_deleted.delete()
            otp.delete()

            return redirect("home:home")

        else:
            form.add_error(field="sms_code", error="کد تایید نامعتبر است.")

            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class OwnerProfileDetailView(AuthenticatedUsersOnlyMixin, OwnerRequiredMixin, URLStorageMixin, DetailView):
    model = CustomUser
    template_name = 'Account/owner_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        exams = Exam.objects.filter(participated_users=user)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context['exams'] = exams
        context['favorite_exams'] = favorite_exams

        return context


class VisitorProfileDetailView(AuthenticatedUsersOnlyMixin, URLStorageMixin, DetailView):
    model = CustomUser
    template_name = 'Account/visitor_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object()
        user = self.request.user

        is_following = Follow.objects.filter(follower=user, following=owner).exists()
        entered_exams = Exam.objects.filter(participated_users=user)

        context['is_following'] = is_following
        context['entered_exams'] = entered_exams

        return context


class ProfileEditView(AuthenticatedUsersOnlyMixin, OwnerRequiredMixin, URLStorageMixin, UpdateView):
    model = CustomUser
    template_name = 'Account/edit_profile.html'
    fields = ("full_name", "email", "about_me")
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = "/"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account:owner_profile', kwargs={'slug': self.request.user.username})


class NotificationListView(AuthenticatedUsersOnlyMixin, URLStorageMixin, ListView):
    model = Notification
    template_name = "Account/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        user = self.request.user

        return Notification.objects.filter(users=user).order_by("-created_at")


class EnterNewsletters(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = None

        if request.user.is_authenticated:
            user = request.user

        if NewsLetter.objects.filter(email=email).exists():
            return JsonResponse({'message': f"این آدرس ایمیل قبلا در خبرنامه ثبت شده است."}, status=400)

        else:
            NewsLetter.objects.create(user=user, email=email)

            return JsonResponse({'message': f"آدرس ایمیل شما با موفقیت در خبرنامه ثبت شد."}, status=200)


class FollowUser(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(CustomUser, username=username)

        if request.user == user_to_follow:
            return JsonResponse({'error': 'شما نمی‌توانید خود را فالو کنید!'}, status=400)

        request.user.follow(user_to_follow)

        return JsonResponse({'message': f"شما {username} را فالو کردید."}, status=200)


class UnfollowUser(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, username):
        user_to_unfollow = get_object_or_404(CustomUser, username=username)

        if request.user == user_to_unfollow:
            return JsonResponse({'error': 'شما نمی‌توانید خود را آن‌فالو کنید!'}, status=400)

        request.user.unfollow(user_to_unfollow)

        return JsonResponse({'message': f"شما {username} را آن‌فالو کردید."}, status=200)


class ParticipatedExams(AuthenticatedUsersOnlyMixin, OwnerRequiredMixin, URLStorageMixin, ListView):
    model = Exam
    template_name = 'Account/participated_exams.html'
    context_object_name = 'exams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context['favorite_exams'] = favorite_exams

        return context

    def get_queryset(self):
        user = self.request.user
        exams = Exam.objects.filter(participated_users=user)

        return exams


class FavoriteExams(AuthenticatedUsersOnlyMixin, OwnerRequiredMixin, URLStorageMixin, ListView):
    model = FavoriteExam
    template_name = 'Account/favorite_exams.html'
    context_object_name = 'exams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context['favorite_exams'] = favorite_exams

        return context

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        user = CustomUser.objects.get(slug=slug)

        exams = FavoriteExam.objects.filter(user=user)

        return exams
