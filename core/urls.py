from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from config.views import ActiveYearLoginView, set_active_year, user_profile

urlpatterns = [
    path('', include('home.urls')),
    path("admin/", admin.site.urls),
    path("accounts/login/", ActiveYearLoginView.as_view(), name="login"),
    path("masuk/", ActiveYearLoginView.as_view(), name="masuk"),
    path("profile/", user_profile, name="user_profile"),
    path("set-active-year/", set_active_year, name="set_active_year"),
    path("", include('admin_berry.urls')),
    path("", include('config.urls')),
    path("", include('menus.urls')),
    path("", include('opd.urls')),
    path("", include('pegawai.urls')),
    path("", include('surat.urls')),
    path("", include('arsip.urls')),
    path("", include('draft.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
