from django.contrib import admin

from .models import (
    DisposisiSurat,
    KlasifikasiSurat,
    LampiranSurat,
    ReviewSurat,
    RiwayatSurat,
    Surat,
    TujuanDisposisi,
)


class LampiranSuratInline(admin.TabularInline):
    model = LampiranSurat
    extra = 0


class ReviewSuratInline(admin.TabularInline):
    model = ReviewSurat
    extra = 0
    readonly_fields = ["dibuat_pada"]


class TujuanDisposisiInline(admin.TabularInline):
    model = TujuanDisposisi
    extra = 0


@admin.register(KlasifikasiSurat)
class KlasifikasiSuratAdmin(admin.ModelAdmin):
    list_display = ["kode", "nama"]
    search_fields = ["kode", "nama"]


@admin.register(Surat)
class SuratAdmin(admin.ModelAdmin):
    list_display = [
        "jenis",
        "nomor_agenda",
        "nomor_surat",
        "tanggal_surat",
        "perihal",
        "sifat",
        "status",
        "unit_pengolah",
    ]
    list_filter = ["jenis", "sifat", "status", "unit_pengolah", "tanggal_surat"]
    search_fields = ["nomor_agenda", "nomor_surat", "perihal", "asal_surat", "tujuan_surat"]
    date_hierarchy = "tanggal_surat"
    inlines = [LampiranSuratInline, ReviewSuratInline]


@admin.register(ReviewSurat)
class ReviewSuratAdmin(admin.ModelAdmin):
    list_display = ["surat", "tahap", "keputusan", "reviewer", "dibuat_pada"]
    list_filter = ["tahap", "keputusan", "dibuat_pada"]
    search_fields = ["surat__nomor_surat", "surat__perihal", "reviewer__nama"]


@admin.register(DisposisiSurat)
class DisposisiSuratAdmin(admin.ModelAdmin):
    list_display = ["nomor_disposisi", "surat", "pemberi", "batas_waktu", "status", "dibuat_pada"]
    list_filter = ["status", "batas_waktu", "dibuat_pada"]
    search_fields = ["nomor_disposisi", "surat__nomor_surat", "surat__perihal", "instruksi"]
    inlines = [TujuanDisposisiInline]


@admin.register(TujuanDisposisi)
class TujuanDisposisiAdmin(admin.ModelAdmin):
    list_display = ["disposisi", "bidang", "penerima", "status", "dibaca_pada", "selesai_pada"]
    list_filter = ["status", "bidang"]
    search_fields = ["disposisi__surat__perihal", "bidang__bidang", "penerima__nama"]


@admin.register(LampiranSurat)
class LampiranSuratAdmin(admin.ModelAdmin):
    list_display = ["surat", "nama", "diunggah_oleh", "diunggah_pada"]
    search_fields = ["surat__nomor_surat", "surat__perihal", "nama"]


@admin.register(RiwayatSurat)
class RiwayatSuratAdmin(admin.ModelAdmin):
    list_display = ["surat", "aksi", "status_sebelum", "status_sesudah", "user", "dibuat_pada"]
    list_filter = ["aksi", "status_sesudah", "dibuat_pada"]
    search_fields = ["surat__nomor_surat", "surat__perihal", "aksi", "keterangan"]
    readonly_fields = ["surat", "aksi", "status_sebelum", "status_sesudah", "keterangan", "user", "dibuat_pada"]
