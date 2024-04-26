from django.urls import path

from Us import views

app_name = 'us'

urlpatterns = [
    path('about', views.AboutView.as_view(), name='about'),
    path('contact', views.Contact.as_view(), name='contact')
]