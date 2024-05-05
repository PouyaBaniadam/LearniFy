import json
import random
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.files.uploadedfile import UploadedFile
from django.core import serializers
from django.db.models import ProtectedError, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView, ListView, View

from Account.forms import OTPRegisterForm, CheckOTPForm, RegularLogin, ForgetPasswordForm, ChangePasswordForm, \
    ChargeWalletForm
from Account.mixins import NonAuthenticatedUsersOnlyMixin, AuthenticatedUsersOnlyMixin, FollowersForPVAccountsOnlyMixin, \
    NonFollowersOnlyMixin, CantChargeWalletYetMixin, CheckFollowingMixin, OwnerOnlyMixin
from Account.models import CustomUser, OTP, Notification, Wallet, NewsLetter, FavoriteVideoCourse, Post, \
    FavoritePDFCourse, Follow
from Account.validator_utilities import validate_mobile_phone_handler
from Course.models import PDFCourse, VideoCourse
from Financial.models import Cart, DepositSlip
from Home.mixins import URLStorageMixin
from utils.useful_functions import summarize_entry


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

        return redirect(reverse("account:check_otp") + f"?uuid={uuid}")

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

        return redirect(reverse("account:profile", kwargs={"slug": request.user.username}))

    def get_success_url(self):
        referring_url = self.request.session.pop(key="referring_url", default=None)
        return referring_url or reverse_lazy("account:profile")


class LogOutView(AuthenticatedUsersOnlyMixin, View):
    def get(self, request):
        redirect_url = request.session.pop('current_url')

        logout(request=request)

        messages.success(request, f"شما با موفقیت از حساب کاربری خود خارج شدید.")

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")


class DeleteAccountView(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        print(user)

        sms_code = random.randint(a=1000, b=9999)
        uuid = str(uuid4())

        OTP.objects.create(username=user.username, mobile_phone=user.mobile_phone, sms_code=sms_code, uuid=uuid,
                           otp_type="D")

        # send_delete_account_sms(receptor=mobile_phone, sms_code=sms_code)
        print(sms_code)
        return redirect(reverse(viewname="account:check_otp") + f"?uuid={uuid}")


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
            return redirect(reverse('account:profile', kwargs={'slug': self.request.user.username}))

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

        return redirect(reverse(viewname="account:check_otp") + f"?uuid={uuid}")


class ProfileEditView(AuthenticatedUsersOnlyMixin, OwnerOnlyMixin, URLStorageMixin, UpdateView):
    model = CustomUser
    template_name = 'Account/edit_profile.html'
    fields = ("full_name", "email", "about_me")
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = "/"

    def form_valid(self, form):
        messages.success(request=self.request, message=f"حساب کاربری شما با موفقیت تغییر یافت.")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account:profile', kwargs={'slug': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        account_status = user.account_status

        context['account_status'] = account_status
        context["mobile_phone"] = user.mobile_phone

        return context


class ChangeMobilePhoneView(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        sms_code = random.randint(a=1000, b=9999)
        username = request.user.username
        user = CustomUser.objects.get(username=username)

        new_mobile_phone = request.POST.get('new_mobile_phone')
        uuid = str(uuid4())

        has_errors = validate_mobile_phone_handler(mobile_phone=new_mobile_phone).get("has_errors")
        message = validate_mobile_phone_handler(mobile_phone=new_mobile_phone).get("message")

        if has_errors:
            error_message = message
            context = {
                "mobile_phone": user.mobile_phone,
                "error_message": error_message,
            }
            return render(request, 'Account/edit_profile.html', context=context)

        if not CustomUser.objects.filter(mobile_phone=new_mobile_phone).exists():
            OTP.objects.create(username=username, mobile_phone=new_mobile_phone, sms_code=sms_code, uuid=uuid,
                               otp_type="UPH")
            # send_register_sms(receptor=mobile_phone, sms_code=sms_code)
            print(sms_code)

            return redirect(reverse("account:check_otp") + f"?uuid={uuid}")

        else:
            error_message = "این شماره تلفن قبلا ثبت شده!"
            context = {
                "mobile_phone": user.mobile_phone,
                "error_message": error_message
            }

            return render(request, 'Account/edit_profile.html', context=context)


class CheckOTPView(FormView):
    form_class = CheckOTPForm
    template_name = 'Account/check_otp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        uuid = request.GET.get('uuid')

        otp = OTP.objects.get(uuid=uuid)
        summarized_mobile_phone = summarize_entry(entry=otp.mobile_phone)

        context["mobile_phone"] = summarized_mobile_phone

        return context

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
            Wallet.objects.create(user=user)
            Cart.objects.create(user=user)

            user.set_password(password)
            user.save()

            login(request=request, user=user)

            otp = OTP.objects.get(uuid=uuid)
            otp.delete()

            messages.success(request, f"{user.username} عزیز، حساب کاربری شما با موفقیت ایجاد شد.")

            return redirect(reverse("account:profile", kwargs={"slug": user.username}))

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="F").exists():
            return redirect(reverse(viewname="account:change_password") + f"?uuid={uuid}")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="D").exists():
            otp = OTP.objects.get(uuid=uuid)
            username = otp.username

            user_to_be_deleted = CustomUser.objects.get(username=username)

            try:
                user_to_be_deleted.delete()
                otp.delete()

                return redirect("home:home")

            except ProtectedError:
                messages.error(request,
                               f"متاسفانه شما مجوز حدف حساب کاربری خود را ندارید. (به دلیل وجود related objects)")

                return redirect(reverse("account:profile", kwargs={"slug": request.user.username}))

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="UPH").exists():
            otp = OTP.objects.get(uuid=uuid)
            mobile_phone = otp.mobile_phone
            username = otp.username

            user = CustomUser.objects.get(username=username)
            user.mobile_phone = mobile_phone
            user.save()

            otp.delete()

            messages.success(request=request, message=f"شماره تلفن با موفقیت تغییر یافت.")

            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        else:
            form.add_error(field="sms_code", error="کد تایید نامعتبر است.")

            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PostListView(FollowersForPVAccountsOnlyMixin, URLStorageMixin, View):
    def get(self, request, slug):
        user = self.request.user
        owner = CustomUser.objects.get(slug=slug)

        if user.is_authenticated:
            user = CustomUser.objects.get(username=user.username)

            is_visitor_the_owner = user == owner  # Checks who is visiting the profile page

            if is_visitor_the_owner:
                posts = Post.objects.filter(user=owner).order_by("-created_at")

                is_following = user.is_following(owner)
                account_status = owner.account_status

                is_follow_request_pending = Notification.objects.filter(
                    users=owner,
                    visibility="PV",
                    following=owner,
                    follower=user,
                    mode="S",
                    type="FO",
                ).exists()

                context = {
                    "posts": posts,
                    "owner": owner,
                    "is_following": is_following,
                    "account_status": account_status,
                    "is_follow_request_pending": is_follow_request_pending,
                }

                return render(request=request, template_name="account/owner_posts.html", context=context)

            else:
                posts = Post.objects.filter(user=owner).order_by("-created_at")

                is_following = user.is_following(owner)
                account_status = owner.account_status

                is_follow_request_pending = Notification.objects.filter(
                    users=owner,
                    visibility="PV",
                    following=owner,
                    follower=user,
                    mode="S",
                    type="FO",
                ).exists()

                context = {
                    "posts": posts,
                    "owner": owner,
                    "is_following": is_following,
                    "account_status": account_status,
                    "is_follow_request_pending": is_follow_request_pending,
                }

                return render(request=request, template_name="account/visitor_posts.html", context=context)

        else:
            posts = Post.objects.filter(user=owner).order_by("-created_at")

            is_following = False
            account_status = owner.account_status

            is_follow_request_pending = False

            context = {
                "posts": posts,
                "owner": owner,
                "is_following": is_following,
                "account_status": account_status,
                "is_follow_request_pending": is_follow_request_pending,
            }

            return render(request=request, template_name="account/visitor_posts.html", context=context)


class TempFollowPrivateAccountFirst(NonFollowersOnlyMixin, URLStorageMixin, View):
    def get(self, request, slug):
        user = self.request.user
        owner = CustomUser.objects.get(slug=slug)

        if user.is_authenticated:
            user = CustomUser.objects.get(username=user.username)

            is_following = user.is_following(owner)
            account_status = owner.account_status

            is_follow_request_pending = Notification.objects.filter(
                users=owner,
                visibility="PV",
                following=owner,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

            context = {
                "user": owner,
                "is_following": is_following,
                "account_status": account_status,
                "is_follow_request_pending": is_follow_request_pending,
            }

            return render(request=request, template_name="account/visitor_posts_blur.html", context=context)

        else:
            is_following = False
            account_status = owner.account_status

            is_follow_request_pending = False

            context = {
                "user": owner,
                "is_following": is_following,
                "account_status": account_status,
                "is_follow_request_pending": is_follow_request_pending,
            }

            return render(request=request, template_name="account/visitor_posts_blur.html", context=context)


@method_decorator(csrf_exempt, name='dispatch')
class ToggleFollow(View):
    def post(self, request):
        username = request.user.username
        follower = CustomUser.objects.get(username=username)

        following_id = request.POST.get("following_id")
        following = CustomUser.objects.get(id=following_id)

        is_following = follower.is_following(following)

        if is_following:
            follower.unfollow(following)

            return JsonResponse(
                data={
                    'message': 'unfollowed',
                    'following_count': following.followers_count()
                },
                status=200
            )

        follower.follow(following)
        return JsonResponse(
            data={
                'message': "followed",
                'following_count': following.followers_count()
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class UnfollowPrivateAccounts(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        follower = CustomUser.objects.get(username=request.user.username)

        following_id = request.POST.get("following_id")

        following = CustomUser.objects.get(id=following_id)

        follower.unfollow(following)

        return JsonResponse(
            data={
                "message": "unfollowed",
                "redirect_url": f""
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class FollowPrivateAccounts(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        follower = CustomUser.objects.get(username=request.user.username)
        following_id = request.POST.get("following_id")

        following = CustomUser.objects.get(id=following_id)

        does_request_exists = Notification.objects.filter(
            users=following,
            title="درخواست فالو",
            visibility="PV",
            following=following,
            follower=follower,
            mode="S",
            type="FO",
        ).exists()

        if does_request_exists:
            Notification.objects.get(
                users=following,
                title="درخواست فالو",
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="FO",
            ).delete()

            return JsonResponse(
                data={
                    "message": "unrequested",
                    "redirect_url": f""
                },
                status=200
            )

        else:
            notification = Notification.objects.create(
                title="درخواست فالو",
                message=f'<p><a href="/account/profile/{follower.username}"><span style="color:hsl(240,75%,60%);">{follower.username}</span></a> می‌خواهد شما را فالو کند.</p>',
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="FO",
            )

            notification.users.add(following)

            notification.save()

            return JsonResponse(
                data={
                    "message": "requested",
                    "redirect_url": f""
                },
                status=200
            )


@method_decorator(csrf_exempt, name='dispatch')
class ToggleAccountStatus(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        username = request.user.username
        user = CustomUser.objects.get(username=username)

        if user.account_status == "PU":
            user.account_status = "PV"
            user.save()

            return JsonResponse(
                {'account_status': "private"},
                status=200
            )

        elif user.account_status == "PV":
            user.account_status = "PU"
            user.save()

            return JsonResponse(
                {'account_status': "public"},
                status=200
            )


class NotificationListView(AuthenticatedUsersOnlyMixin, URLStorageMixin, ListView):
    model = Notification
    template_name = "Account/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        user = self.request.user

        return Notification.objects.filter(users=user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        account_status = user.account_status

        context['account_status'] = account_status

        return context


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


class FavoriteVideoCourses(AuthenticatedUsersOnlyMixin, URLStorageMixin, ListView):
    model = FavoriteVideoCourse
    template_name = 'Account/favorite_videos.html'
    context_object_name = 'video_courses'

    def get_queryset(self):
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        video_courses = FavoriteVideoCourse.objects.filter(user=user)

        return video_courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        account_status = user.account_status

        context['account_status'] = account_status

        return context


class FavoritePDFCourses(AuthenticatedUsersOnlyMixin, URLStorageMixin, ListView):
    model = FavoritePDFCourse
    template_name = 'Account/favorite_pdfs.html'
    context_object_name = 'pdf_courses'

    def get_queryset(self):
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        pdf_courses = FavoritePDFCourse.objects.filter(user=user)

        return pdf_courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user = CustomUser.objects.get(username=user.username)

        account_status = user.account_status

        context['account_status'] = account_status

        return context


@method_decorator(csrf_exempt, name='dispatch')
class HandleFollowRequests(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        follower = request.POST.get('follower')
        following = request.POST.get('following')
        mode = request.POST.get('mode')

        follower = CustomUser.objects.get(username=follower)
        following = CustomUser.objects.get(username=following)

        if mode == 'ACC':
            notification = Notification.objects.get(
                users=following,
                title="درخواست فالو",
                visibility="PV",
                following=following,
                follower=follower,
                mode="S",
                type="FO",
            )
            notification.delete()

            follower.follow(following)

            return JsonResponse(
                data={
                    "message": "accepted",
                    "message_text": f'<p><a href="/account/profile/{follower.username}"><span style="color:hsl(240,75%,60%);">{follower.username}</span></a> شما را فالو کرد.</p>'
                },
                status=200
            )

        notification = Notification.objects.get(
            users=following,
            title="درخواست فالو",
            visibility="PV",
            following=following,
            follower=follower,
            mode="S",
            type="FO",
        )
        notification.delete()

        return JsonResponse(
            data={
                "message": "rejected"
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class AddPostView(View):
    def post(self, request):
        if request.method == 'POST':
            image = request.FILES.get('image')
            title = request.POST.get('title')
            caption = request.POST.get('caption')

            if len(title) > 50:
                return JsonResponse(
                    data={
                        "error": "موضوع نباید بیشتر از 50 کاراکتر داشته باشد.",
                    },
                    status=400
                )

            if len(caption) > 1000:
                return JsonResponse(
                    data={
                        "error": "کپشن نباید بیشتر از 1000 کاراکتر داشته باشد.",
                    },
                    status=400
                )

            if not image or not isinstance(image, UploadedFile):
                return JsonResponse({'error': 'هیچ فایلی ارائه نشده!'}, status=400)

            max_size_bytes = 2048 * 1024
            if image.size > max_size_bytes:
                return JsonResponse({'error': 'تصویر نباید بیشتر از 2 مگابایت حجم داشته باشد.'}, status=400)

            if request.user.is_authenticated:
                Post.objects.create(
                    user=request.user,
                    title=title,
                    caption=caption,
                    file=image
                )
                return JsonResponse({'message': 'پست با موفقیت ساخته شد.'}, status=200)
            else:
                return JsonResponse({'error': 'لطفا ابتدا وارد شوید.'}, status=401)

        return JsonResponse({'error': 'Invalid request method'}, status=405)


@method_decorator(csrf_exempt, name='dispatch')
class DeletePostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_id = data.get('postId')

            if post_id is not None:
                post = get_object_or_404(Post, id=post_id)
                post.delete()
                return JsonResponse({'message': 'Post deleted successfully.'})
            else:
                return JsonResponse({'error': 'Invalid postId'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCaptionView(View):
    def post(self, request):
        data = json.loads(request.body)
        post_id = data.get('post_id')
        caption = data.get('caption')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse(
                data={
                    'message': 'Post not found',
                },
                status=404
            )

        post.caption = caption
        post.save()

        if request.user != post.user:
            return JsonResponse(
                data={
                    'message': 'Denied',
                },
                status=403
            )
        else:
            return JsonResponse(
                data={
                    'message': 'Done',
                    'caption': caption
                },
                status=200
            )


@method_decorator(csrf_exempt, name='dispatch')
class ChargeWallet(AuthenticatedUsersOnlyMixin, CantChargeWalletYetMixin, FormView):
    form_class = ChargeWalletForm
    template_name = "Account/charge_wallet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        redirect_url = self.request.session.get('current_url')

        context["redirect_url"] = redirect_url

        return context

    def post(self, request, *args, **kwargs):
        image = self.request.FILES.get('image')
        username = self.request.user.username

        user = CustomUser.objects.get(username=username)

        DepositSlip.objects.create(
            user=user,
            receipt=image,
            type="WAL",
            total_cost=0
        )

        return JsonResponse(
            data={
                "message": "فیش واریزی با موفقیت آپلود شد.",
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class FollowersList(AuthenticatedUsersOnlyMixin, CheckFollowingMixin, View):
    def post(self, request, *args, **kwargs):
        owner_id = request.POST.get('owner')
        owner = CustomUser.objects.get(id=owner_id)

        followers_qs = Follow.objects.filter(following=owner)
        followers_list = []
        for follower_username, follower_image, follower_stars in followers_qs.values_list("follower__username",
                                                                                          "follower__image",
                                                                                          "follower__stars"):
            if follower_image:
                follower_image_url = f"{settings.MEDIA_URL}{follower_image}"
            else:
                follower_image_url = static('../assets/images/avatars/default_user.JPG')
            followers_list.append((follower_username, follower_image_url, follower_stars))

        return JsonResponse(
            data={
                "followers": followers_list
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class FollowingList(AuthenticatedUsersOnlyMixin, CheckFollowingMixin, View):
    def post(self, request, *args, **kwargs):
        owner_id = request.POST.get('owner')
        owner = CustomUser.objects.get(id=owner_id)

        followings_qs = Follow.objects.filter(follower=owner).select_related('following')
        followings_list = []
        for following in followings_qs:
            following_username = following.following.username
            following_image = following.following.image.url if following.following.image else static(
                '../assets/images/avatars/default_user.JPG')
            following_stars = following.following.stars
            followings_list.append((following_username, following_image, following_stars))

        return JsonResponse(
            data={
                "followings": followings_list
            },
            status=200
        )


class UserPDFCourseListView(FollowersForPVAccountsOnlyMixin, ListView):
    model = PDFCourse
    context_object_name = 'pdf_courses'

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        pdf_courses = PDFCourse.objects.filter(teacher__slug=slug)

        return pdf_courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        slug = self.kwargs.get("slug")
        owner = CustomUser.objects.get(slug=slug)

        if user.is_authenticated:
            user = CustomUser.objects.get(username=user.username)
            is_following = user.is_following(owner)
            account_status = owner.account_status

            is_follow_request_pending = Notification.objects.filter(
                users=owner,
                visibility="PV",
                following=owner,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            is_following = False
            account_status = owner.account_status

            is_follow_request_pending = False

        favorite_pdf_courses = PDFCourse.favorite_pdf_list(self, user=user)

        context['favorite_pdf_courses'] = favorite_pdf_courses
        context['user'] = user
        context['owner'] = owner
        context['is_following'] = is_following
        context['account_status'] = account_status
        context['is_follow_request_pending'] = is_follow_request_pending

        return context

    def get_template_names(self):
        user = self.request.user
        slug = self.kwargs.get("slug")

        owner = CustomUser.objects.get(slug=slug)

        if owner == user:
            return ['Account/owner_pdf_courses.html']

        else:
            return ['Account/visitor_pdf_courses.html']


class UserVideoCourseListView(FollowersForPVAccountsOnlyMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        video_courses = VideoCourse.objects.filter(teacher__slug=slug)

        return video_courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        slug = self.kwargs.get("slug")
        owner = CustomUser.objects.get(slug=slug)

        if user.is_authenticated:
            user = CustomUser.objects.get(username=user.username)
            is_following = user.is_following(owner)
            account_status = owner.account_status

            is_follow_request_pending = Notification.objects.filter(
                users=owner,
                visibility="PV",
                following=owner,
                follower=user,
                mode="S",
                type="FO",
            ).exists()

        else:
            is_following = False
            account_status = owner.account_status

            is_follow_request_pending = False

        favorite_video_courses = VideoCourse.favorite_video_list(self, user=user)

        context['favorite_video_courses'] = favorite_video_courses
        context['user'] = user
        context['owner'] = owner
        context['is_following'] = is_following
        context['account_status'] = account_status
        context['is_follow_request_pending'] = is_follow_request_pending

        return context

    def get_template_names(self):
        user = self.request.user
        slug = self.kwargs.get("slug")

        owner = CustomUser.objects.get(slug=slug)

        if owner == user:
            return ['Account/owner_video_courses.html']

        else:
            return ['Account/visitor_video_courses.html']


def search_view(request):
    query = request.GET.get('query', '')

    results = CustomUser.objects.filter(Q(username__icontains=query) | Q(full_name__icontains=query))

    serialized_results = []
    for user in results:
        serialized_user = {
            'slug': user.slug,
            'username': user.username
        }
        serialized_results.append(serialized_user)

    return JsonResponse(
        data={
            'results': serialized_results
        },
        status=200
    )
