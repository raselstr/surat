from django.urls import path

from .views import JenisDokumenListView, DraftSuratListView, UndanganListView, TujuanSuratListView

urlpatterns = [
    path("jenis_dokumen/", JenisDokumenListView.as_view(), name="jenis_dokumen_list"),
    path("jenis_dokumen/add/", JenisDokumenListView.as_view(), name="jenis_dokumen_add"),
    path("jenis_dokumen/<int:pk>/form/", JenisDokumenListView.as_view(), name="jenis_dokumen_update"),
    path("jenis_dokumen/<int:pk>/delete/", JenisDokumenListView.as_view(), name="jenis_dokumen_delete"),

    path("draft_surat/", DraftSuratListView.as_view(), name="draft_surat_list"),
    path("draft_surat/add/", DraftSuratListView.as_view(), name="draft_surat_add"),
    path("draft_surat/<int:pk>/form/", DraftSuratListView.as_view(), name="draft_surat_update"),
    path("draft_surat/<int:pk>/delete/", DraftSuratListView.as_view(), name="draft_surat_delete"),

    path("undangan/", UndanganListView.as_view(), name="undangan_list"),
    path("undangan/add/", UndanganListView.as_view(), name="undangan_add"),
    path("undangan/<int:pk>/form/", UndanganListView.as_view(), name="undangan_update"),
    path("undangan/<int:pk>/delete/", UndanganListView.as_view(), name="undangan_delete"),

    path("tujuan_surat/", TujuanSuratListView.as_view(), name="tujuan_surat_list"),
    path("tujuan_surat/add/", TujuanSuratListView.as_view(), name="tujuan_surat_add"),
    path("tujuan_surat/<int:pk>/form/", TujuanSuratListView.as_view(), name="tujuan_surat_update"),
    path("tujuan_surat/<int:pk>/delete/", TujuanSuratListView.as_view(), name="tujuan_surat_delete"),
]