from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('videos', views.AllVideoCourses.as_view(), name='all_video_courses'),
    path('video/register/', views.RegisterInVideoCourse.as_view(), name='register_video_course'),
    path('videos/filter', views.VideoCourseFilterView.as_view(), name='filter_video_courses'),
    path('video/<slug>', views.VideoCourseDetail.as_view(), name='video_course_detail'),
    path('videos/category/<slug>', views.VideoCourseByCategory.as_view(), name='videos_by_category'),
    path('video/favorite/toggle/', views.ToggleFavorite.as_view(), name='toggle_favorite'),
    path('video/add/comment/<slug>', views.AddVideoCourseComment.as_view(), name='add_video_course_comment'),
    path('video/comment/delete/<id>', views.DeleteVideoCourseComment.as_view(), name='delete_video_course_comment'),
    path('video/like_comment/', views.LikeVideoCourseComment.as_view(), name='like_video_course_comment'),
    path('exam/<slug>/enter', views.EnterExam.as_view(), name='enter_exam'),
    path('exam/<slug>', views.ExamDetail.as_view(), name='exam_detail'),
    path('books', views.AllBookCourses.as_view(), name='all_book_courses'),
    path('exam/<slug>/submit/final', views.FinalExamSubmit.as_view(), name='final_exam_submit'),
    path('exam/<slug>/calculate/result', views.CalculateExamResult.as_view(), name='calculate_exam_result'),
]
