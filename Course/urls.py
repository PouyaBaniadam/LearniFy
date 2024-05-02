from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('videos', views.AllVideoCourses.as_view(), name='all_video_courses'),
    path('video/register/', views.RegisterInVideoCourse.as_view(), name='register_video_course'),
    path('videos/filter', views.VideoCourseFilterView.as_view(), name='filter_video_courses'),
    path('video/<slug>', views.VideoCourseDetail.as_view(), name='video_course_detail'),
    path('video/<slug>/episodes', views.VideoCourseEpisodes.as_view(), name='video_course_episodes'),
    path('videos/category/<slug>', views.VideoCourseByCategory.as_view(), name='videos_by_category'),
    path('video/<slug>/download/', views.VideoCourseDownloadSession.as_view(), name='download_video_session'),
    path('video/favorite/toggle/', views.ToggleVideoCourseFavorite.as_view(), name='toggle_video_course_favorite'),
    path('video/add/comment/<slug>', views.AddVideoCourseComment.as_view(), name='add_video_course_comment'),
    path('video/favorite/toggle/', views.ToggleVideoCourseFavorite.as_view(), name='video_toggle_favorite'),
    path('video/comment/delete/<id>', views.DeleteVideoCourseComment.as_view(), name='delete_video_course_comment'),
    path('video/like_comment/', views.LikeVideoCourseComment.as_view(), name='like_video_course_comment'),
    path('pdfs', views.AllPDFCourses.as_view(), name='all_pdf_courses'),
    path('pdf/register/', views.RegisterInPDFCourse.as_view(), name='register_pdf_course'),
    path('pdfs/filter', views.PDFCourseFilterView.as_view(), name='filter_pdf_courses'),
    path('pdf/<slug>', views.PDFCourseDetail.as_view(), name='pdf_course_detail'),
    path('pdf/<slug>/episodes', views.PDFCourseEpisodes.as_view(), name='pdf_course_episodes'),
    path('pdf/<slug>/download/', views.PDFCourseDownloadSession.as_view(), name='download_pdf_session'),
    path('pdfs/category/<slug>', views.PDFCourseByCategory.as_view(), name='pdfs_by_category'),
    path('pdf/favorite/toggle/', views.TogglePDFCourseFavorite.as_view(), name='pdf_toggle_favorite'),
    path('pdf/add/comment/<slug>', views.AddPDFCourseComment.as_view(), name='add_pdf_course_comment'),
    path('pdf/comment/delete/<id>', views.DeletePDFCourseComment.as_view(), name='delete_pdf_course_comment'),
    path('pdf/like_comment/', views.LikePDFCourseComment.as_view(), name='like_pdf_course_comment'),
    path('exam/<slug>/enter', views.EnterExam.as_view(), name='enter_exam'),
    path('exam/<slug>', views.ExamDetail.as_view(), name='exam_detail'),
    path('exam/<slug>/submit/final', views.FinalExamSubmit.as_view(), name='final_exam_submit'),
    path('exam/<slug>/calculate/result', views.CalculateExamResult.as_view(), name='calculate_exam_result'),
]
