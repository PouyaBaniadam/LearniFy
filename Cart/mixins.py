from Account.models import CustomUser


class ParticipatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        discount_code = request.POST.get("discount_code")
        user = request.user

        user = CustomUser.objects.get(username=user.username)

        if not can_user_participate:
            redirect_url = request.session.get('current_url')

            messages.error(request, f"ابتدا در آزمون ثبت نام کنید!")

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)
