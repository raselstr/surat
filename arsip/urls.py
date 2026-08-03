from django.urls import path

from .views import KlasifikasiListView, KategoriListView, UnitListView, InformasiListView
urlpatterns = [
    path("klasifikasi/", KlasifikasiListView.as_view(), name="klasifikasi_list"),
    path("klasifikasi/add/", KlasifikasiListView.as_view(), name="klasifikasi_add"),
    path("klasifikasi/<int:pk>/form/", KlasifikasiListView.as_view(), name="klasifikasi_update"),
    path("klasifikasi/<int:pk>/delete/", KlasifikasiListView.as_view(), name="klasifikasi_delete"),

    path("kategori/", KategoriListView.as_view(), name="kategori_list"),
    path("kategori/add/", KategoriListView.as_view(), name="kategori_add"),
    path("kategori/<int:pk>/form/", KategoriListView.as_view(), name="kategori_update"),
    path("kategori/<int:pk>/delete/", KategoriListView.as_view(), name="kategori_delete"),

    path("unit/", UnitListView.as_view(), name="unit_list"),
    path("unit/add/", UnitListView.as_view(), name="unit_add"),
    path("unit/<int:pk>/form/", UnitListView.as_view(), name="unit_update"),
    path("unit/<int:pk>/delete/", UnitListView.as_view(), name="unit_delete"),

    path("informasi/", InformasiListView.as_view(), name="informasi_list"),
    path("informasi/add/", InformasiListView.as_view(), name="informasi_add"),
    path("informasi/<int:pk>/form/", InformasiListView.as_view(), name="informasi_update"),
    path("informasi/<int:pk>/delete/", InformasiListView.as_view(), name="informasi_delete"),
]

