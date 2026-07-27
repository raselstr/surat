from django.urls import path

from .views import PegawaiListView, BidangListView, EselonListView, PangkatListView

urlpatterns = [
    path("bidang/", BidangListView.as_view(), name="bidang_list"),
    path("bidang/add/", BidangListView.as_view(), name="bidang_add"),
    path("bidang/<int:pk>/form/", BidangListView.as_view(), name="bidang_update"),
    path("bidang/<int:pk>/delete/", BidangListView.as_view(), name="bidang_delete"),

    path("eselon/", EselonListView.as_view(), name="eselon_list"),
    path("eselon/add/", EselonListView.as_view(), name="eselon_add"),
    path("eselon/<int:pk>/form/", EselonListView.as_view(), name="eselon_update"),
    path("eselon/<int:pk>/delete/", EselonListView.as_view(), name="eselon_delete"),

    path("pangkat/", PangkatListView.as_view(), name="pangkat_list"),
    path("pangkat/add/", PangkatListView.as_view(), name="pangkat_add"),
    path("pangkat/<int:pk>/form/", PangkatListView.as_view(), name="pangkat_update"),
    path("pangkat/<int:pk>/delete/", PangkatListView.as_view(), name="pangkat_delete"),

    path("pegawai/", PegawaiListView.as_view(), name="pegawai_list"),
    path("pegawai/add/", PegawaiListView.as_view(), name="pegawai_add"),
    path("pegawai/<int:pk>/form/", PegawaiListView.as_view(), name="pegawai_update"),
    path("pegawai/<int:pk>/delete/", PegawaiListView.as_view(), name="pegawai_delete"),
]