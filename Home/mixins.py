from django.views.generic.base import View


class URLStorageMixin(View):
    def dispatch(self, request, *args, **kwargs):
        current_url = request.build_absolute_uri()

        request.session['current_url'] = current_url

        return super().dispatch(request, *args, **kwargs)
