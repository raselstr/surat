from django.db import models


class OPD(models.Model):
    kode = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)

    class Meta:
        verbose_name = "OPD"
        verbose_name_plural = "OPD"
        ordering = ["kode"]

    def __str__(self):
        return self.nama


class SubOPD(models.Model):
    kode = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)
    opd = models.ForeignKey(OPD, on_delete=models.CASCADE, related_name="sub_opds")

    class Meta:
        verbose_name = "Sub OPD"
        verbose_name_plural = "Sub OPD"
        ordering = ["kode"]

    def __str__(self):
        return f"{self.nama} ({self.opd.nama})"
