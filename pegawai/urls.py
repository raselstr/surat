from django.urls import path

from .views import PegawaiListView

urlpatterns = [
    path("pegawai/", PegawaiListView.as_view(), name="pegawai_list"),
    path("pegawai/add/", PegawaiListView.as_view(), name="pegawai_add"),
    path("pegawai/<int:pk>/form/", PegawaiListView.as_view(), name="pegawai_update"),
    path("pegawai/<int:pk>/delete/", PegawaiListView.as_view(), name="pegawai_delete"),
]