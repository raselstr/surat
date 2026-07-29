from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from types import SimpleNamespace

from config.crud.base import FullAccessCRUDView

from .forms import (
    DisposisiCepatForm,
    DisposisiSuratForm,
    KlasifikasiSuratForm,
    LampiranSuratForm,
    ReviewSuratForm,
    RiwayatSuratForm,
    SuratKeluarForm,
    SuratMasukForm,
    TujuanDisposisiForm,
    VerifikasiSuratForm,
)
from .models import (
    DisposisiSurat,
    KlasifikasiSurat,
    LampiranSurat,
    ReviewSurat,
    RiwayatSurat,
    Surat,
    TujuanDisposisi,
)
from .tables import (
    DisposisiSuratTable,
    KlasifikasiSuratTable,
    LampiranSuratTable,
    ReviewSuratTable,
    RiwayatSuratTable,
    SuratKeluarTable,
    SuratMasukTable,
    TujuanDisposisiTable,
)


def catat_riwayat(surat, aksi, user=None, status_sebelum="", status_sesudah="", keterangan=""):
    RiwayatSurat.objects.create(
        surat=surat,
        aksi=aksi,
        status_sebelum=status_sebelum or "",
        status_sesudah=status_sesudah or surat.status,
        keterangan=keterangan,
        user=user if getattr(user, "is_authenticated", False) else None,
    )


def ubah_status_surat(surat, status_baru, aksi, user=None, keterangan=""):
    status_lama = surat.status
    surat.status = status_baru
    surat.diperbarui_oleh = user if getattr(user, "is_authenticated", False) else None
    surat.save(update_fields=["status", "diperbarui_oleh", "diperbarui_pada"])
    catat_riwayat(
        surat,
        aksi,
        user=user,
        status_sebelum=status_lama,
        status_sesudah=status_baru,
        keterangan=keterangan,
    )


class KlasifikasiSuratListView(FullAccessCRUDView):
    model = KlasifikasiSurat
    form_class = KlasifikasiSuratForm
    table_class = KlasifikasiSuratTable
    title = "Klasifikasi Surat"
    url_list = "/klasifikasi-surat/"
    url_action = "/klasifikasi-surat/"
    url_action_pk = "/klasifikasi-surat/"
    enable_year_filter = False


class SuratMasukListView(FullAccessCRUDView):
    model = Surat
    form_class = SuratMasukForm
    table_class = SuratMasukTable
    title = "Surat Masuk"
    url_list = "/surat-masuk/"
    url_action = "/surat-masuk/"
    url_action_pk = "/surat-masuk/"

    def get_base_queryset(self):
        return (
            Surat.objects.filter(jenis=Surat.Jenis.MASUK)
            .select_related("klasifikasi", "unit_pengolah", "bidang_pembuat", "penanggung_jawab")
            .order_by("-tanggal_surat", "-id")
        )


class SuratKeluarListView(FullAccessCRUDView):
    model = Surat
    form_class = SuratKeluarForm
    table_class = SuratKeluarTable
    title = "Surat Keluar"
    url_list = "/surat-keluar/"
    url_action = "/surat-keluar/"
    url_action_pk = "/surat-keluar/"

    def get_base_queryset(self):
        return (
            Surat.objects.filter(jenis=Surat.Jenis.KELUAR)
            .select_related("klasifikasi", "unit_pengolah", "bidang_pembuat", "penanggung_jawab")
            .order_by("-tanggal_surat", "-id")
        )


class ReviewSuratListView(FullAccessCRUDView):
    model = ReviewSurat
    form_class = ReviewSuratForm
    table_class = ReviewSuratTable
    title = "Review Surat"
    url_list = "/review-surat/"
    url_action = "/review-surat/"
    url_action_pk = "/review-surat/"

    def get_base_queryset(self):
        return ReviewSurat.objects.select_related("surat", "reviewer", "user").order_by("-dibuat_pada")


class DisposisiSuratListView(FullAccessCRUDView):
    model = DisposisiSurat
    form_class = DisposisiSuratForm
    table_class = DisposisiSuratTable
    title = "Disposisi Surat"
    url_list = "/disposisi-surat/"
    url_action = "/disposisi-surat/"
    url_action_pk = "/disposisi-surat/"

    def get_base_queryset(self):
        return (
            DisposisiSurat.objects.select_related("surat", "pemberi", "dibuat_oleh")
            .prefetch_related("tujuan")
            .order_by("-dibuat_pada")
        )


class TujuanDisposisiListView(FullAccessCRUDView):
    model = TujuanDisposisi
    form_class = TujuanDisposisiForm
    table_class = TujuanDisposisiTable
    title = "Tujuan Disposisi"
    url_list = "/tujuan-disposisi/"
    url_action = "/tujuan-disposisi/"
    url_action_pk = "/tujuan-disposisi/"

    def get_base_queryset(self):
        return TujuanDisposisi.objects.select_related(
            "disposisi",
            "disposisi__surat",
            "bidang",
            "penerima",
        )


class LampiranSuratListView(FullAccessCRUDView):
    model = LampiranSurat
    form_class = LampiranSuratForm
    table_class = LampiranSuratTable
    title = "Lampiran Surat"
    url_list = "/lampiran-surat/"
    url_action = "/lampiran-surat/"
    url_action_pk = "/lampiran-surat/"

    def get_base_queryset(self):
        return LampiranSurat.objects.select_related("surat", "diunggah_oleh").order_by("-diunggah_pada")


class RiwayatSuratListView(FullAccessCRUDView):
    model = RiwayatSurat
    form_class = RiwayatSuratForm
    table_class = RiwayatSuratTable
    title = "Riwayat Surat"
    url_list = "/riwayat-surat/"
    url_action = "/riwayat-surat/"
    url_action_pk = "/riwayat-surat/"
    use_crud_modal = False

    def get_base_queryset(self):
        return RiwayatSurat.objects.select_related("surat", "user").order_by("-dibuat_pada")

    def get_permission(self):
        return SimpleNamespace(can_view=True, can_add=False, can_edit=False, can_delete=False)


@login_required
@require_http_methods(["POST"])
def ajukan_surat(request, pk):
    surat = get_object_or_404(Surat, pk=pk)
    if surat.status not in [Surat.Status.DRAFT, Surat.Status.DIKEMBALIKAN]:
        messages.warning(request, "Surat hanya dapat diajukan dari status draft atau dikembalikan.")
        return redirect(_surat_redirect_url(surat))

    ubah_status_surat(
        surat,
        Surat.Status.DIAJUKAN,
        "Diajukan staf",
        user=request.user,
    )
    messages.success(request, "Surat berhasil diajukan.")
    return redirect(_surat_redirect_url(surat))


@login_required
@require_http_methods(["GET", "POST"])
def verifikasi_surat(request, pk):
    return _review_action(
        request,
        pk,
        title="Verifikasi Kasi",
        tahap=ReviewSurat.Tahap.VERIFIKASI_KASI,
        status_setuju=Surat.Status.DIVERIFIKASI_KASI,
        aksi_setuju="Diverifikasi Kasi",
    )


@login_required
@require_http_methods(["GET", "POST"])
def validasi_sekretaris_surat(request, pk):
    return _review_action(
        request,
        pk,
        title="Validasi Sekretaris",
        tahap=ReviewSurat.Tahap.VALIDASI_SEKRETARIS,
        status_setuju=Surat.Status.DIVALIDASI,
        aksi_setuju="Divalidasi Sekretaris",
    )


@login_required
@require_http_methods(["GET", "POST"])
def validasi_kepala_surat(request, pk):
    return _review_action(
        request,
        pk,
        title="Validasi Kepala",
        tahap=ReviewSurat.Tahap.VALIDASI_KEPALA,
        status_setuju=Surat.Status.DIVALIDASI,
        aksi_setuju="Divalidasi Kepala",
    )


def _review_action(request, pk, title, tahap, status_setuju, aksi_setuju):
    surat = get_object_or_404(Surat, pk=pk)
    form = VerifikasiSuratForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        keputusan = form.cleaned_data["keputusan"]
        catatan = form.cleaned_data["catatan"]

        with transaction.atomic():
            ReviewSurat.objects.create(
                surat=surat,
                tahap=tahap,
                keputusan=keputusan,
                catatan=catatan,
                reviewer=form.cleaned_data["reviewer"],
                user=request.user,
            )

            if keputusan == ReviewSurat.Keputusan.SETUJU:
                ubah_status_surat(
                    surat,
                    status_setuju,
                    aksi_setuju,
                    user=request.user,
                    keterangan=catatan,
                )
                messages.success(request, f"Surat berhasil {aksi_setuju.lower()}.")
            else:
                ubah_status_surat(
                    surat,
                    Surat.Status.DIKEMBALIKAN,
                    "Dikembalikan untuk perbaikan",
                    user=request.user,
                    keterangan=catatan,
                )
                messages.warning(request, "Surat dikembalikan untuk perbaikan.")

        return redirect(_surat_redirect_url(surat))

    return render(request, "components/crud/form_page.html", {
        "form": form,
        "title": title,
        "url_list": _surat_redirect_url(surat),
        "form_action": request.path,
        "submit_label": "Simpan Keputusan",
        "use_modal": False,
        "template_form": "components/crud/form_general.html",
    })


@login_required
@require_http_methods(["GET", "POST"])
def disposisi_cepat_surat(request, pk):
    surat = get_object_or_404(Surat, pk=pk)
    form = DisposisiCepatForm(request.POST or None, request=request, surat=surat)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            disposisi = form.save()
            surat_status = Surat.Status.DIDISPOSISI
            if disposisi.status == DisposisiSurat.Status.DIKIRIM:
                surat_status = Surat.Status.DIDISTRIBUSIKAN

            ubah_status_surat(
                surat,
                surat_status,
                "Didisposisikan",
                user=request.user,
                keterangan=disposisi.instruksi,
            )
            disposisi.dikirim_pada = timezone.now()
            disposisi.save(update_fields=["dikirim_pada"])

        messages.success(request, "Disposisi berhasil dibuat dan dikirim ke bidang tujuan.")
        return redirect("disposisi_surat_list")

    return render(request, "components/crud/form_page.html", {
        "form": form,
        "title": "Disposisi Surat",
        "url_list": _surat_redirect_url(surat),
        "form_action": request.path,
        "submit_label": "Kirim Disposisi",
        "use_modal": False,
        "template_form": "components/crud/form_general.html",
    })


def _surat_redirect_url(surat):
    if surat.jenis == Surat.Jenis.KELUAR:
        return "/surat-keluar/"
    return "/surat-masuk/"
