from django.db import models

class Klasifikasi(models.Model):
    kode = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Klasifikasi"
        verbose_name_plural = "Klasifikasi"

    def __str__(self):
        return self.nama

class Kategori(models.Model):
    klasifikasi = models.ForeignKey(Klasifikasi, on_delete=models.CASCADE, related_name="kategori")
    kode = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"

    def __str__(self):
        return self.nama

class Unit(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name="unit")
    kode = models.CharField(max_length=30, unique=True)
    nama = models.TextField()

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Unit"

    def __str__(self):
        return self.nama

class Informasi(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="informasi")
    kode = models.CharField(max_length=30, unique=True)
    nama = models.TextField()

    class Meta:
        verbose_name = "Informasi"
        verbose_name_plural = "Informasi"

    def __str__(self):
        return self.nama
    
