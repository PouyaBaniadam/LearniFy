from django.urls import path

from Home import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("search", views.SearchView.as_view(), name="search"),
]
