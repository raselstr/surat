import django_tables2 as tables
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils.html import format_html

from config.tables import BaseTable, action_column

from .models import (
    DisposisiSurat,
    KlasifikasiSurat,
    LampiranSurat,
    ReviewSurat,
    RiwayatSurat,
    Surat,
    TujuanDisposisi,
)


class KlasifikasiSuratTable(BaseTable):
    aksi = action_column("klasifikasi_surat_update", "klasifikasi_surat_delete")

    class Meta(BaseTable.Meta):
        model = KlasifikasiSurat
        fields = ("no", "kode", "nama", "keterangan", "aksi")
        order_by = ("kode",)


class SuratTable(BaseTable):
    alur = tables.Column(empty_values=(), verbose_name="Alur", orderable=False)
    aksi = action_column("surat_update", "surat_delete")

    class Meta(BaseTable.Meta):
        model = Surat
        fields = (
            "no",
            "nomor_agenda",
            "nomor_surat",
            "tanggal_surat",
            "asal_surat",
            "tujuan_surat",
            "perihal",
            "sifat",
            "status",
            "alur",
            "unit_pengolah",
            "aksi",
        )
        order_by = ("-tanggal_surat", "-id")

    def render_alur(self, record):
        request = getattr(self, "request", None)
        csrf_token = get_token(request) if request else ""

        if record.status in [Surat.Status.DRAFT, Surat.Status.DIKEMBALIKAN]:
            return format_html(
                (
                    '<form method="post" action="{}" style="display:inline;">'
                    '<input type="hidden" name="csrfmiddlewaretoken" value="{}">'
                    '<button type="submit" class="btn btn-sm btn-outline-primary">Ajukan</button>'
                    '</form>'
                ),
                reverse("surat_ajukan", args=[record.pk]),
                csrf_token,
            )

        if record.status == Surat.Status.DIAJUKAN:
            return format_html(
                '<a class="btn btn-sm btn-outline-primary" href="{}">Verifikasi</a>',
                reverse("surat_verifikasi", args=[record.pk]),
            )

        if record.status == Surat.Status.DIVERIFIKASI_KASI:
            return format_html(
                (
                    '<a class="btn btn-sm btn-outline-primary me-1" href="{}">Validasi Sekretaris</a>'
                    '<a class="btn btn-sm btn-outline-primary" href="{}">Validasi Kepala</a>'
                ),
                reverse("surat_validasi_sekretaris", args=[record.pk]),
                reverse("surat_validasi_kepala", args=[record.pk]),
            )

        if record.status == Surat.Status.DIVALIDASI:
            return format_html(
                '<a class="btn btn-sm btn-outline-primary" href="{}">Disposisi</a>',
                reverse("surat_disposisi_cepat", args=[record.pk]),
            )

        return "-"


class SuratMasukTable(SuratTable):
    aksi = action_column("surat_masuk_update", "surat_masuk_delete")

    class Meta(SuratTable.Meta):
        fields = (
            "no",
            "nomor_agenda",
            "nomor_surat",
            "tanggal_surat",
            "tanggal_diterima",
            "asal_surat",
            "perihal",
            "sifat",
            "status",
            "alur",
            "aksi",
        )


class SuratKeluarTable(SuratTable):
    aksi = action_column("surat_keluar_update", "surat_keluar_delete")

    class Meta(SuratTable.Meta):
        fields = (
            "no",
            "nomor_agenda",
            "nomor_surat",
            "tanggal_surat",
            "tanggal_dikirim",
            "tujuan_surat",
            "perihal",
            "sifat",
            "status",
            "alur",
            "aksi",
        )


class ReviewSuratTable(BaseTable):
    aksi = action_column("review_surat_update", "review_surat_delete")

    class Meta(BaseTable.Meta):
        model = ReviewSurat
        fields = ("no", "surat", "tahap", "keputusan", "reviewer", "dibuat_pada", "aksi")
        order_by = ("-dibuat_pada",)


class DisposisiSuratTable(BaseTable):
    jumlah_tujuan = tables.Column(empty_values=(), verbose_name="Tujuan")
    aksi = action_column("disposisi_surat_update", "disposisi_surat_delete")

    class Meta(BaseTable.Meta):
        model = DisposisiSurat
        fields = (
            "no",
            "nomor_disposisi",
            "surat",
            "pemberi",
            "batas_waktu",
            "status",
            "jumlah_tujuan",
            "aksi",
        )
        order_by = ("-dibuat_pada",)

    def render_jumlah_tujuan(self, record):
        return record.tujuan.count()


class TujuanDisposisiTable(BaseTable):
    aksi = action_column("tujuan_disposisi_update", "tujuan_disposisi_delete")

    class Meta(BaseTable.Meta):
        model = TujuanDisposisi
        fields = (
            "no",
            "disposisi",
            "bidang",
            "penerima",
            "status",
            "dibaca_pada",
            "selesai_pada",
            "aksi",
        )
        order_by = ("disposisi", "bidang__bidang")


class LampiranSuratTable(BaseTable):
    aksi = action_column("lampiran_surat_update", "lampiran_surat_delete")

    class Meta(BaseTable.Meta):
        model = LampiranSurat
        fields = ("no", "surat", "nama", "berkas", "diunggah_oleh", "diunggah_pada", "aksi")
        order_by = ("-diunggah_pada",)


class RiwayatSuratTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = RiwayatSurat
        fields = (
            "no",
            "surat",
            "aksi",
            "status_sebelum",
            "status_sesudah",
            "user",
            "dibuat_pada",
        )
        order_by = ("-dibuat_pada",)
