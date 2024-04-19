from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from Account.models import CustomUser


class NonAuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        redirect_url = request.session.get('current_url')

        if request.user.is_authenticated:
            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super(NonAuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class AuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدار وارد حساب کاربری خود شوید.")

            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super(AuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class FollowersForPVAccountsOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')
        owner = CustomUser.objects.get(slug=slug)

        if owner != request.user:
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

        return super(FollowersForPVAccountsOnlyMixin, self).dispatch(request, *args, **kwargs)


class NonFollowersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')
        owner = CustomUser.objects.get(slug=slug)

        if owner != request.user:
            if user.is_authenticated:
                user = CustomUser.objects.get(username=user.username)
                if owner.account_status == "PV" and user.id in owner.followers.all().values_list(
                        "follower_id", flat=True
                ):
                    messages.error(request, f"شما مجوز ورود به این صفحه را ندارید!")

                    redirect_url = request.session.get('current_url')
                    print(redirect_url)

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
