"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
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
]
