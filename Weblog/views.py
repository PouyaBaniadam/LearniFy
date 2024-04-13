import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, View
from hitcount.views import HitCountDetailView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Account.models import CustomUser
from Home.mixins import URLStorageMixin
from Weblog.models import Weblog, Comment


class AllWeblogs(URLStorageMixin, ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblog_list.html'

    def get_queryset(self):
        weblogs = Weblog.objects.select_related('category', 'author').order_by('-created_at')

        return weblogs


class WeblogDetail(URLStorageMixin, HitCountDetailView, DetailView):
    model = Weblog
    context_object_name = 'weblog'
    template_name = 'Weblog/weblog_detail.html'
    count_hit = True

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        comments = self.object.weblog_comments.all()

        if self.request.user.is_authenticated:
            user_likes = Comment.objects.filter(likes=user).values_list('id', flat=True)

        else:
            user_likes = []

        related_weblogs = self.object.get_related_weblogs(max_results=5)
        latest_weblogs = self.object.get_latest_weblogs()

        context['comments'] = comments
        context['user_likes'] = user_likes
        context['related_weblogs'] = related_weblogs
        context['latest_weblogs'] = latest_weblogs

        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class WeblogsByCategory(URLStorageMixin, ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblogs_by_category.html'
    paginate_by = 6

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        weblogs = get_list_or_404(Weblog, category__slug=slug)

        return weblogs


class AddComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        slug = kwargs.get('slug')

        weblog = get_object_or_404(Weblog, slug=slug)

        Comment.objects.create(user=user, text=text, weblog=weblog, parent_id=parent_id)
        messages.success(request, f"نظر شما با موفقیت ثبت شد.")

        fragment = 'reply_section'
        url = reverse('weblog:detail', kwargs={'slug': slug}) + f'#{fragment}'

        return redirect(url)


class DeleteComment(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        comment = Comment.objects.get(id=id)
        weblog = Weblog.objects.get(weblog_comments=comment)
        comment.delete()

        messages.success(request, f"نظر شما با موفقیت حذف شد.")

        return redirect(reverse("weblog:detail", kwargs={'slug': weblog.slug}))


class LikeCommentView(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')

            comment = get_object_or_404(Comment, id=comment_id)
            user = request.user

            if user in comment.likes.all():
                comment.likes.remove(user)
                liked = False
            else:
                comment.likes.add(user)
                liked = True

            return JsonResponse({'liked': liked})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'چنین کامنتی یافت نشد.'}, status=404)
