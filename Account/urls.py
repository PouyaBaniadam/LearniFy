from django.urls import path

from Account import views

app_name = "account"

urlpatterns = [
    path("profile/<slug:slug>", views.ProfileDetailView.as_view(), name="profile"),
    path("profile/<slug:slug>/edit", views.ProfileEditView.as_view(), name="edit_profile"),
    path("login", views.LogInView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("check/otp", views.CheckOTPView.as_view(), name="check_otp"),
    path("password/forget", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("password/change", views.ChangePasswordView.as_view(), name="change_password"),
    path("notifications", views.NotificationListView.as_view(), name="notifications"),
    path("enter_newsletters", views.EnterNewsletters.as_view(), name="enter_newsletters"),
    path('toggle/follow/', views.ToggleFollow.as_view(), name='toggle_follow'),
    path('toggle/follow/private/accounts/', views.FollowPrivateAccounts.as_view(), name='follow_private_accounts'),
    path('unfollow/private/accounts/', views.UnfollowPrivateAccounts.as_view(), name='unfollow_private_accounts'),
    path('toggle/account/status/', views.ToggleAccountStatus.as_view(), name='toggle_account_status'),
    path('favorite/<slug:slug>', views.FavoriteCourses.as_view(), name='favorites'),
]
