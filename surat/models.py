from django.conf import settings
from django.db import models
from django.utils import timezone


class KlasifikasiSurat(models.Model):
    kode = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=150)
    keterangan = models.TextField(blank=True)

    class Meta:
        verbose_name = "Klasifikasi Surat"
        verbose_name_plural = "Klasifikasi Surat"
        ordering = ["kode"]

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Surat(models.Model):
    class Jenis(models.TextChoices):
        MASUK = "masuk", "Surat Masuk"
        KELUAR = "keluar", "Surat Keluar"

    class Sifat(models.TextChoices):
        BIASA = "biasa", "Biasa"
        PENTING = "penting", "Penting"
        SEGERA = "segera", "Segera"
        SANGAT_SEGERA = "sangat_segera", "Sangat Segera"
        RAHASIA = "rahasia", "Rahasia"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        DIAJUKAN = "diajukan", "Diajukan Staf"
        DIVERIFIKASI_KASI = "diverifikasi_kasi", "Diverifikasi Kasi"
        DIKEMBALIKAN = "dikembalikan", "Dikembalikan"
        DIVALIDASI = "divalidasi", "Divalidasi"
        DIDISPOSISI = "didisposisi", "Didisposisi"
        DIDISTRIBUSIKAN = "didistribusikan", "Didistribusikan"
        SELESAI = "selesai", "Selesai"
        DIARSIPKAN = "diarsipkan", "Diarsipkan"

    jenis = models.CharField(max_length=10, choices=Jenis.choices)
    nomor_agenda = models.CharField(max_length=50, blank=True)
    nomor_surat = models.CharField(max_length=100, blank=True)
    tanggal_surat = models.DateField()
    tanggal_diterima = models.DateField(null=True, blank=True)
    tanggal_dikirim = models.DateField(null=True, blank=True)

    asal_surat = models.CharField(max_length=255, blank=True)
    tujuan_surat = models.CharField(max_length=255, blank=True)
    perihal = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True)

    klasifikasi = models.ForeignKey(
        KlasifikasiSurat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surat",
    )
    sifat = models.CharField(max_length=20, choices=Sifat.choices, default=Sifat.BIASA)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)

    unit_pengolah = models.ForeignKey(
        "opd.SubOPD",
        on_delete=models.PROTECT,
        related_name="surat_unit_pengolah",
    )
    bidang_pembuat = models.ForeignKey(
        "pegawai.Bidang",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surat_dibuat",
    )
    penanggung_jawab = models.ForeignKey(
        "pegawai.Pegawai",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surat_tanggung_jawab",
    )

    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="surat_dibuat",
    )
    diperbarui_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="surat_diperbarui",
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Surat"
        verbose_name_plural = "Surat"
        ordering = ["-tanggal_surat", "-id"]
        indexes = [
            models.Index(fields=["jenis", "status"]),
            models.Index(fields=["nomor_agenda"]),
            models.Index(fields=["nomor_surat"]),
            models.Index(fields=["tanggal_surat"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["jenis", "nomor_agenda", "unit_pengolah"],
                condition=~models.Q(nomor_agenda=""),
                name="uniq_nomor_agenda_per_jenis_unit",
            ),
            models.UniqueConstraint(
                fields=["jenis", "nomor_surat", "unit_pengolah"],
                condition=~models.Q(nomor_surat=""),
                name="uniq_nomor_surat_per_jenis_unit",
            ),
        ]

    def __str__(self):
        nomor = self.nomor_surat or self.nomor_agenda or "-"
        return f"{self.get_jenis_display()} {nomor} - {self.perihal}"


class ReviewSurat(models.Model):
    class Tahap(models.TextChoices):
        VERIFIKASI_KASI = "verifikasi_kasi", "Verifikasi Kasi"
        VALIDASI_SEKRETARIS = "validasi_sekretaris", "Validasi Sekretaris"
        VALIDASI_KEPALA = "validasi_kepala", "Validasi Kepala"

    class Keputusan(models.TextChoices):
        SETUJU = "setuju", "Setuju"
        REVISI = "revisi", "Revisi"
        TOLAK = "tolak", "Tolak"

    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name="review")
    tahap = models.CharField(max_length=30, choices=Tahap.choices)
    keputusan = models.CharField(max_length=10, choices=Keputusan.choices)
    catatan = models.TextField(blank=True)
    reviewer = models.ForeignKey(
        "pegawai.Pegawai",
        on_delete=models.PROTECT,
        related_name="review_surat",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="review_surat",
    )
    dibuat_pada = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Review Surat"
        verbose_name_plural = "Review Surat"
        ordering = ["surat", "dibuat_pada"]
        indexes = [
            models.Index(fields=["tahap", "keputusan"]),
            models.Index(fields=["dibuat_pada"]),
        ]

    def __str__(self):
        return f"{self.surat} - {self.get_tahap_display()} - {self.get_keputusan_display()}"


class DisposisiSurat(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        DIKIRIM = "dikirim", "Dikirim"
        DITINDAKLANJUTI = "ditindaklanjuti", "Ditindaklanjuti"
        SELESAI = "selesai", "Selesai"

    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name="disposisi")
    nomor_disposisi = models.CharField(max_length=50, blank=True)
    pemberi = models.ForeignKey(
        "pegawai.Pegawai",
        on_delete=models.PROTECT,
        related_name="disposisi_diberikan",
    )
    instruksi = models.TextField()
    catatan = models.TextField(blank=True)
    batas_waktu = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="disposisi_dibuat",
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    dikirim_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Disposisi Surat"
        verbose_name_plural = "Disposisi Surat"
        ordering = ["-dibuat_pada"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["batas_waktu"]),
        ]

    def __str__(self):
        nomor = self.nomor_disposisi or self.surat.nomor_surat or self.surat.nomor_agenda
        return f"Disposisi {nomor}"


class TujuanDisposisi(models.Model):
    class Status(models.TextChoices):
        BELUM_DIBACA = "belum_dibaca", "Belum Dibaca"
        DIBACA = "dibaca", "Dibaca"
        DIPROSES = "diproses", "Diproses"
        SELESAI = "selesai", "Selesai"

    disposisi = models.ForeignKey(
        DisposisiSurat,
        on_delete=models.CASCADE,
        related_name="tujuan",
    )
    bidang = models.ForeignKey(
        "pegawai.Bidang",
        on_delete=models.PROTECT,
        related_name="tujuan_disposisi",
    )
    penerima = models.ForeignKey(
        "pegawai.Pegawai",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tujuan_disposisi",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BELUM_DIBACA)
    catatan_tindak_lanjut = models.TextField(blank=True)
    dibaca_pada = models.DateTimeField(null=True, blank=True)
    selesai_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Tujuan Disposisi"
        verbose_name_plural = "Tujuan Disposisi"
        ordering = ["disposisi", "bidang__bidang"]
        constraints = [
            models.UniqueConstraint(
                fields=["disposisi", "bidang"],
                name="uniq_bidang_per_disposisi",
            ),
        ]

    def __str__(self):
        return f"{self.disposisi} -> {self.bidang}"


class LampiranSurat(models.Model):
    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name="lampiran")
    nama = models.CharField(max_length=150)
    berkas = models.FileField(upload_to="surat/lampiran/%Y/%m/")
    keterangan = models.CharField(max_length=255, blank=True)
    diunggah_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="lampiran_surat",
    )
    diunggah_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lampiran Surat"
        verbose_name_plural = "Lampiran Surat"
        ordering = ["surat", "nama"]

    def __str__(self):
        return self.nama


class RiwayatSurat(models.Model):
    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name="riwayat")
    aksi = models.CharField(max_length=100)
    status_sebelum = models.CharField(max_length=30, blank=True)
    status_sesudah = models.CharField(max_length=30, blank=True)
    keterangan = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="riwayat_surat",
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Riwayat Surat"
        verbose_name_plural = "Riwayat Surat"
        ordering = ["-dibuat_pada"]
        indexes = [
            models.Index(fields=["aksi"]),
            models.Index(fields=["dibuat_pada"]),
        ]

    def __str__(self):
        return f"{self.surat} - {self.aksi}"
