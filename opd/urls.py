from django.urls import path

from .views import OPDListView, SubOPDListView, PenandatanganListView, PemdaListView, KopSuratListView

urlpatterns = [
    path("opd/", OPDListView.as_view(), name="opd_list"),
    path("opd/add/", OPDListView.as_view(), name="opd_add"),
    path("opd/<int:pk>/form/", OPDListView.as_view(), name="opd_update"),
    path("opd/<int:pk>/delete/", OPDListView.as_view(), name="opd_delete"),

    path("sub-opd/", SubOPDListView.as_view(), name="subopd_list"),
    path("sub-opd/add/", SubOPDListView.as_view(), name="subopd_add"),
    path("sub-opd/<int:pk>/form/", SubOPDListView.as_view(), name="subopd_update"),
    path("sub-opd/<int:pk>/delete/", SubOPDListView.as_view(), name="subopd_delete"),

    path("penandatangan/", PenandatanganListView.as_view(), name="penandatangan_list"),
    path("penandatangan/add/", PenandatanganListView.as_view(), name="penandatangan_add"),
    path("penandatangan/<int:pk>/form/", PenandatanganListView.as_view(), name="penandatangan_update"),
    path("penandatangan/<int:pk>/delete/", PenandatanganListView.as_view(), name="penandatangan_delete"),

    path("pemda/", PemdaListView.as_view(), name="pemda_list"),
    path("pemda/add/", PemdaListView.as_view(), name="pemda_add"),
    path("pemda/<int:pk>/form/", PemdaListView.as_view(), name="pemda_update"),
    path("pemda/<int:pk>/delete/", PemdaListView.as_view(), name="pemda_delete"),

    path("kop-surat/", KopSuratListView.as_view(), name="kopsurat_list"),
    path("kop-surat/add/", KopSuratListView.as_view(), name="kopsurat_add"),
    path("kop-surat/<int:pk>/form/", KopSuratListView.as_view(), name="kopsurat_update"),
    path("kop-surat/<int:pk>/delete/", KopSuratListView.as_view(), name="kopsurat_delete"),
]
