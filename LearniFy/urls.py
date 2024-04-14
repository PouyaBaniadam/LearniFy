from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from LearniFy import settings

urlpatterns = ([
                   path("i18n/", include("django.conf.urls.i18n")),
                   path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
                   path("__debug__/", include("debug_toolbar.urls")),
                   path('ratings/', include("star_ratings.urls", namespace="ratings")),
                   path('hitcount/', include("hitcount.urls", namespace="hitcount")),
                   path('', include('Home.urls')),
                   path('account/', include('Account.urls')),
                   path('course/', include('Course.urls')),
                   path('news/', include('News.urls')),
                   path('weblog/', include('Weblog.urls')),
                   path('us/', include('Us.urls')),
                   path('cart/', include('Cart.urls')),
               ]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
urlpatterns += i18n_patterns(path("admin/", admin.site.urls))
