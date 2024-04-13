from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


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


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs['slug']

        if user.username != slug:
            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                messages.error(request, f"شما اجازه دسترسی به این صفحه را ندارید!")

                return redirect(redirect_url)

            return redirect(reverse("account:owner_profile", kwargs={'slug': user.username}))

        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)