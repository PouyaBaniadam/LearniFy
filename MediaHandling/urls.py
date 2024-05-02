from django.urls import path

from MediaHandling import views

app_name = 'media_handling'

urlpatterns = [
    path('<path:filepath>', views.serve_protected_media, name='file_handling'),
]
