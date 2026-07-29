from django.urls import path

from .views import (
    DisposisiSuratListView,
    KlasifikasiSuratListView,
    LampiranSuratListView,
    ReviewSuratListView,
    RiwayatSuratListView,
    SuratKeluarListView,
    SuratMasukListView,
    TujuanDisposisiListView,
    ajukan_surat,
    disposisi_cepat_surat,
    validasi_kepala_surat,
    validasi_sekretaris_surat,
    verifikasi_surat,
)


urlpatterns = [
    path("klasifikasi-surat/", KlasifikasiSuratListView.as_view(), name="klasifikasi_surat_list"),
    path("klasifikasi-surat/add/", KlasifikasiSuratListView.as_view(), name="klasifikasi_surat_add"),
    path("klasifikasi-surat/<int:pk>/form/", KlasifikasiSuratListView.as_view(), name="klasifikasi_surat_update"),
    path("klasifikasi-surat/<int:pk>/delete/", KlasifikasiSuratListView.as_view(), name="klasifikasi_surat_delete"),

    path("surat-masuk/", SuratMasukListView.as_view(), name="surat_masuk_list"),
    path("surat-masuk/add/", SuratMasukListView.as_view(), name="surat_masuk_add"),
    path("surat-masuk/<int:pk>/form/", SuratMasukListView.as_view(), name="surat_masuk_update"),
    path("surat-masuk/<int:pk>/delete/", SuratMasukListView.as_view(), name="surat_masuk_delete"),

    path("surat-keluar/", SuratKeluarListView.as_view(), name="surat_keluar_list"),
    path("surat-keluar/add/", SuratKeluarListView.as_view(), name="surat_keluar_add"),
    path("surat-keluar/<int:pk>/form/", SuratKeluarListView.as_view(), name="surat_keluar_update"),
    path("surat-keluar/<int:pk>/delete/", SuratKeluarListView.as_view(), name="surat_keluar_delete"),

    path("surat/<int:pk>/ajukan/", ajukan_surat, name="surat_ajukan"),
    path("surat/<int:pk>/verifikasi/", verifikasi_surat, name="surat_verifikasi"),
    path("surat/<int:pk>/validasi-sekretaris/", validasi_sekretaris_surat, name="surat_validasi_sekretaris"),
    path("surat/<int:pk>/validasi-kepala/", validasi_kepala_surat, name="surat_validasi_kepala"),
    path("surat/<int:pk>/disposisi/", disposisi_cepat_surat, name="surat_disposisi_cepat"),

    path("review-surat/", ReviewSuratListView.as_view(), name="review_surat_list"),
    path("review-surat/add/", ReviewSuratListView.as_view(), name="review_surat_add"),
    path("review-surat/<int:pk>/form/", ReviewSuratListView.as_view(), name="review_surat_update"),
    path("review-surat/<int:pk>/delete/", ReviewSuratListView.as_view(), name="review_surat_delete"),

    path("disposisi-surat/", DisposisiSuratListView.as_view(), name="disposisi_surat_list"),
    path("disposisi-surat/add/", DisposisiSuratListView.as_view(), name="disposisi_surat_add"),
    path("disposisi-surat/<int:pk>/form/", DisposisiSuratListView.as_view(), name="disposisi_surat_update"),
    path("disposisi-surat/<int:pk>/delete/", DisposisiSuratListView.as_view(), name="disposisi_surat_delete"),

    path("tujuan-disposisi/", TujuanDisposisiListView.as_view(), name="tujuan_disposisi_list"),
    path("tujuan-disposisi/add/", TujuanDisposisiListView.as_view(), name="tujuan_disposisi_add"),
    path("tujuan-disposisi/<int:pk>/form/", TujuanDisposisiListView.as_view(), name="tujuan_disposisi_update"),
    path("tujuan-disposisi/<int:pk>/delete/", TujuanDisposisiListView.as_view(), name="tujuan_disposisi_delete"),

    path("lampiran-surat/", LampiranSuratListView.as_view(), name="lampiran_surat_list"),
    path("lampiran-surat/add/", LampiranSuratListView.as_view(), name="lampiran_surat_add"),
    path("lampiran-surat/<int:pk>/form/", LampiranSuratListView.as_view(), name="lampiran_surat_update"),
    path("lampiran-surat/<int:pk>/delete/", LampiranSuratListView.as_view(), name="lampiran_surat_delete"),

    path("riwayat-surat/", RiwayatSuratListView.as_view(), name="riwayat_surat_list"),
]
