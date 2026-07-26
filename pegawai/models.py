from django.db import models

class Pangkat(models.Model):
    pangkat = models.CharField(max_length=255)
    golongan = models.CharField(max_length=10)
    ruang = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Pangkat"
        verbose_name_plural = "Pangkat"
        ordering = ["pangkat"]

    def __str__(self):
        return f"{self.pangkat}/ ({self.golongan}.{self.ruang})"

class Eselon(models.Model):
    eselon = models.CharField(max_length=255)
    urutan = models.IntegerField()

    class Meta:
        verbose_name = "Eselon"
        verbose_name_plural = "Eselon"
        ordering = ["urutan"]

    def __str__(self):
        return f"{self.eselon}"

class Pegawai(models.Model):
    nip = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE, related_name="pegawais")
    sub_opd = models.ForeignKey('opd.SubOPD', on_delete=models.CASCADE, related_name="pegawais")

    class Meta:
        verbose_name = "Pegawai"
        verbose_name_plural = "Pegawai"
        ordering = ["nip"]

    def __str__(self):
        return f"{self.nama} ({self.nip})"

