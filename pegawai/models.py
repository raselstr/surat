from django.db import models

class Pegawai(models.Model):
    nip = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)
    sub_opd = models.ForeignKey('opd.SubOPD', on_delete=models.CASCADE, related_name="pegawais")

    class Meta:
        verbose_name = "Pegawai"
        verbose_name_plural = "Pegawai"
        ordering = ["nip"]

    def __str__(self):
        return f"{self.nama} ({self.nip})"
