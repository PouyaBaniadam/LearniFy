from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from Account.models import CustomUser, TempChargeWallet
from Financial.models import DepositSlip


class NonAuthenticatedUsersOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        redirect_url = request.session.get('current_url')

        if request.user.is_authenticated:
            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super(NonAuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class AuthenticatedUsersOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدار وارد حساب کاربری خود شوید.")

            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super(AuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class FollowersForPVAccountsOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        slug = kwargs.get('slug')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            try:
                owner = CustomUser.objects.get(slug=slug)
                if owner.account_status == "PV":
                    messages.error(request, "جهت ورود به این صفحه، ابتدا باید کاربر را فالو کنید.")

                    return redirect(reverse("account:temp_follow", kwargs={"slug": owner.slug}))

            except CustomUser.DoesNotExist:
                messages.error(request, f"چنین کاربری یافت نشد!")

                redirect_url = request.session.get('current_url')

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        try:
            owner = CustomUser.objects.get(slug=slug)

            if owner != user:
                if user.is_authenticated:
                    user = CustomUser.objects.get(username=user.username)
                    if owner.account_status == "PV" and user.id not in owner.followers.all().values_list(
                            "follower_id", flat=True
                    ):
                        messages.error(request, "جهت ورود به این صفحه، ابتدا باید کاربر را فالو کنید.")

                        return redirect(reverse("account:temp_follow", kwargs={"slug": owner.slug}))

                else:
                    if owner.account_status == "PV":
                        messages.error(request, "جهت ورود به این صفحه، ابتدا باید کاربر را فالو کنید.")

                        return redirect(reverse("account:temp_follow", kwargs={"slug": owner.slug}))

        except CustomUser.DoesNotExist:
            messages.error(request, f"چنین کاربری یافت نشد!")

            redirect_url = request.session.get('current_url')

            if user.is_authenticated:
                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        except UnboundLocalError:
            pass

        return super(FollowersForPVAccountsOnlyMixin, self).dispatch(request, *args, **kwargs)


class NonFollowersOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')
        owner = CustomUser.objects.get(slug=slug)

        if owner != request.user:
            if user.is_authenticated:
                user = CustomUser.objects.get(username=user.username)
                if owner.account_status == "PU" or user.is_following(owner):
                    messages.error(request, f"شما مجوز ورود به این صفحه را ندارید!")

                    redirect_url = request.session.get('current_url')

                    if redirect_url is not None:
                        if request.resolver_match.url_name != "temp_follow":
                            return redirect(redirect_url)

                        else:
                            return redirect(reverse("account:profile", kwargs={"slug": owner.slug}))

                    return redirect("home:home")

        else:
            messages.error(request, f"شما مجوز ورود به این صفحه را ندارید!")

            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                if request.resolver_match.url_name != "temp_follow":
                    return redirect(redirect_url)

                else:
                    return redirect(reverse("account:profile", kwargs={"slug": owner.slug}))

            return redirect("home:home")

        return super(NonFollowersOnlyMixin, self).dispatch(request, *args, **kwargs)


class OwnerOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get("slug")

        if request.user.username != slug:
            messages.error(request, f"شما اجازه دسترسی به این صفحه را ندارید!")

            redirect_url = request.session.get('current_url')

            if request.user.is_authenticated:
                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        return super(OwnerOnlyMixin, self).dispatch(request, *args, **kwargs)


class CantChargeWalletYetMixin(View):
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        user = CustomUser.objects.get(username=username)

        if DepositSlip.objects.filter(
                user=user,
                type="WAL",
                is_valid=False
        ).exists():
            messages.error(request, f"تیم پشتیبانی در حال بررسی درخواست قبلی شما می‌‌باشد.")

            redirect_url = request.session.get('current_url')

            if request.user.is_authenticated:
                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        return super(CantChargeWalletYetMixin, self).dispatch(request, *args, **kwargs)


class CheckFollowingMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user_id = request.POST.get('user')
        owner_id = request.POST.get('owner')

        user = CustomUser.objects.get(id=user_id)
        owner = CustomUser.objects.get(id=owner_id)

        if owner.account_status == "PV" and not user.is_following(owner) and user != owner:
            return JsonResponse(
                data={
                    "error": "شما مجوز مشاهده این بخش ندارید."
                },
                status=400
            )

        return super(CheckFollowingMixin, self).dispatch(request, *args, **kwargs)


class DeleteTempChargeWalletMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        temp_charge_wallets = TempChargeWallet.objects.filter(user=user)
        if temp_charge_wallets.count() != 0:
            for temp_charge_wallet in temp_charge_wallets:
                temp_charge_wallet.delete()

        return super().dispatch(request, *args, **kwargs)