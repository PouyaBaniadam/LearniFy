from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from Account.models import CustomUser


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
                if owner.account_status == "PV" and user.id in owner.followers.all().values_list(
                        "follower_id", flat=True
                ):
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
