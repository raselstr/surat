from django.db import models

class JenisDokumen(models.Model):
    nama = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Jenis Dokumen"
        verbose_name_plural = "Jenis Dokumen"

    def __str__(self):
        return self.nama

class DraftSurat(models.Model):
    jenis_dokumen = models.ForeignKey(
        JenisDokumen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='draft_surat'
    )
    nomor = models.CharField(max_length=30, unique=True)
    sifat = models.CharField(max_length=255)
    lampiran = models.CharField(max_length=255)
    hal = models.CharField(max_length=255)
    dari = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    pembuka = models.TextField()
    isi = models.TextField()
    penutup = models.TextField()
    tembusan = models.TextField()
    pejabat_penandatangan = models.ForeignKey(
        "opd.Penandatangan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='draft_surat'
    )

    class Meta:
        verbose_name = "Draft Surat"
        verbose_name_plural = "Draft Surat"

    def __str__(self):
        return self.hal

class Undangan(models.Model):
    draft_surat = models.OneToOneField(
        DraftSurat,
        on_delete=models.CASCADE,
        related_name='undangan'
    )
    tanggalmulai = models.DateField()
    tanggalselesai = models.DateField()
    jammulai = models.TimeField()
    jamselesai = models.CharField(max_length=255)
    tempat = models.CharField(max_length=255)
    agenda = models.TextField()
    perlengkapan = models.TextField()

    class Meta:
        verbose_name = "Undangan"
        verbose_name_plural = "Undangan"

    def __str__(self):
        return f"Undangan {self.draft_surat.hal}"
    
class TujuanSurat(models.Model):
    draft_surat = models.OneToOneField(
        DraftSurat,
        on_delete=models.CASCADE,
        related_name='tujuansurat'
    )
    instansi = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tujuan Surat"
        verbose_name_plural = "Tujuan Surat"

    def __str__(self):
        return f"Tujuan Surat {self.draft_surat.hal}"