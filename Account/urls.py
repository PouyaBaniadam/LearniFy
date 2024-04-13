from django.urls import path

from Account import views

app_name = "account"

urlpatterns = [
    path("profile/owner/<slug:slug>", views.OwnerProfileDetailView.as_view(), name="owner_profile"),
    path("profile/visitor/<slug:slug>", views.OwnerProfileDetailView.as_view(), name="visitor_profile"),
    path("profile/<slug:slug>/edit", views.ProfileEditView.as_view(), name="edit_profile"),
    path("login", views.LogInView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("check/otp", views.CheckOTPView.as_view(), name="check_otp"),
    path("password/forget", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("password/change", views.ChangePasswordView.as_view(), name="change_password"),
    path("notifications", views.NotificationListView.as_view(), name="notifications"),
    path("enter_newsletters", views.EnterNewsletters.as_view(), name="enter_newsletters"),
    path('follow/<str:username>/', views.FollowUser.as_view(), name='follow_user'),
    path('unfollow/<str:username>/', views.UnfollowUser.as_view(), name='unfollow_user'),
    path('participated/exams/<slug:slug>', views.ParticipatedExams.as_view(), name='participated_exams'),
    path('favorite/exams/<slug:slug>', views.FavoriteExams.as_view(), name='favorite_exams'),
]
