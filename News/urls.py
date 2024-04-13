from django.urls import path

from News import views

app_name = 'news'

urlpatterns = [
    path('list', views.AllNews.as_view(), name='all'),
    path('detail/<slug>', views.NewsDetail.as_view(), name='detail'),
    path('category/<slug>', views.NewsByCategory.as_view(), name='by_category'),
    path('add/comment/<slug>', views.AddComment.as_view(), name='add_comment'),
    path('comment/delete/<id>', views.DeleteComment.as_view(), name='delete_comment'),
    path('like_comment/', views.LikeCommentView.as_view(), name='like_comment'),
]
