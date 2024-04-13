import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView, View
from hitcount.views import HitCountDetailView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Home.mixins import URLStorageMixin
from News.models import News, Comment


class AllNews(URLStorageMixin, ListView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_list.html'

    def get_queryset(self):
        news = News.objects.select_related('category', 'author').order_by('-created_at')

        return news


class NewsDetail(URLStorageMixin, HitCountDetailView, DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_detail.html'
    count_hit = True

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        comments = self.object.news_comments.all()

        if self.request.user.is_authenticated:
            user_likes = Comment.objects.filter(likes=user).values_list('id', flat=True)

        else:
            user_likes = []

        related_news = self.object.get_related_news(max_results=5)
        latest_news = self.object.get_latest_news()

        context['comments'] = comments
        context['user_likes'] = user_likes
        context['related_news'] = related_news
        context['latest_news'] = latest_news

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class NewsByCategory(URLStorageMixin, ListView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        news = get_list_or_404(News, category__slug=slug)

        return news


class AddComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        slug = kwargs.get('slug')

        news = get_object_or_404(News, slug=slug)

        Comment.objects.create(user=user, text=text, news=news, parent_id=parent_id)
        messages.success(request, f"نظر شما با موفقیت ثبت شد.")

        fragment = 'reply_section'
        url = reverse('news:detail', kwargs={'slug': slug}) + f'#{fragment}'

        return redirect(url)


class DeleteComment(AuthenticatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        comment = Comment.objects.get(id=id)
        news = News.objects.get(news_comments=comment)
        comment.delete()

        messages.success(request, f"نظر شما با موفقیت حذف شد.")

        return redirect(reverse("news:detail", kwargs={'slug': news.slug}))


class LikeCommentView(AuthenticatedUsersOnlyMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')
            print(comment_id)

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
