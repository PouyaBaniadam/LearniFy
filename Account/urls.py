from django.urls import path

from Account import views

app_name = "account"

urlpatterns = [
    path("profile/<slug:slug>", views.PostListView.as_view(), name="profile"),
    path("profile/post/add/", views.AddPostView.as_view(), name="add_post"),
    path("profile/post/delete/", views.DeletePostView.as_view(), name="delete_post"),
    path("profile/post/caption/update/", views.UpdateCaptionView.as_view(), name="update_caption"),
    path("profile/<slug:slug>/temp/follow", views.TempFollowPrivateAccountFirst.as_view(), name="temp_follow"),
    path("profile/videos/<slug:slug>", views.VideoCoursesView.as_view(), name="video_courses"),
    path("profile/<slug:slug>/edit", views.ProfileEditView.as_view(), name="edit_profile"),
    path("login", views.LogInView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("check/otp", views.CheckOTPView.as_view(), name="check_otp"),
    path("password/forget", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("password/change", views.ChangePasswordView.as_view(), name="change_password"),
    path("mobile_phone/change", views.ChangeMobilePhoneView.as_view(), name="change_mobile_phone"),
    path("notifications", views.NotificationListView.as_view(), name="notifications"),
    path("enter_newsletters", views.EnterNewsletters.as_view(), name="enter_newsletters"),
    path('toggle/follow/', views.ToggleFollow.as_view(), name='toggle_follow'),
    path('toggle/follow/private/accounts/', views.FollowPrivateAccounts.as_view(), name='follow_private_accounts'),
    path('unfollow/private/accounts/', views.UnfollowPrivateAccounts.as_view(), name='unfollow_private_accounts'),
    path('handle/follow/requests/', views.HandleFollowRequests.as_view(), name='handle_follow_requests'),
    path('toggle/account/status/', views.ToggleAccountStatus.as_view(), name='toggle_account_status'),
    path('favorite/videos/', views.FavoriteVideoCourses.as_view(), name='favorite_videos'),
    path('favorite/pdfs/', views.FavoritePDFCourses.as_view(), name='favorite_pdfs'),
    path('wallet/charge/', views.ChargeWallet.as_view(), name='charge_wallet'),
    path('followers/list/', views.FollowersList.as_view(), name='followers_list'),
    path('followings/list/', views.FollowingList.as_view(), name='followings_list'),
]
