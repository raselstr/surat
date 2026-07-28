from django.db import models

class Pangkat(models.Model):
    pangkat = models.CharField(max_length=255)
    golongan = models.CharField(max_length=10)
    ruang = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Pangkat"
        verbose_name_plural = "Pangkat"
        constraints = [
            models.UniqueConstraint(
                fields=['pangkat', 'golongan', 'ruang'],
                name='unique_pangkat_golongan_ruang'
            )
        ]

    def __str__(self):
        if self.ruang:
            return f"{self.pangkat} / {self.golongan}.{self.ruang}"
        return f"{self.pangkat} / {self.golongan}"

class Eselon(models.Model):
    eselon = models.CharField(max_length=255)
    urutan = models.IntegerField()

    class Meta:
        verbose_name = "Eselon"
        verbose_name_plural = "Eselon"

    def __str__(self):
        return f"{self.eselon}"

class JenisJabatan(models.Model):
    nama = models.CharField(max_length=150, unique=True)
    keterangan= models.CharField(max_length=200, null=True, blank=True)
    fungsi= models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Jenis Jabatan"
        verbose_name_plural = "Jenis Jabatan"

    def __str__(self):
        return self.nama

class StatusASN(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Status ASN"
        verbose_name_plural = "Status ASN"

    def __str__(self):
        return self.nama

class Bidang(models.Model):
    bidang = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Bidang"
        verbose_name_plural = "Bidang"

    def __str__(self):
        return f"{self.bidang}"

class Tugas(models.Model):
    nama = models.CharField(max_length=200, unique=True)
    keterangan = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Tugas"
        verbose_name_plural = "Tugas"

    def __str__(self):
        return self.nama

class Tingkat(models.Model):
    tingkat = models.CharField(max_length=100, unique=True)
    ket = models.CharField(max_length=200, null=True, blank=True)
    pesawat = models.CharField(max_length=100, null=True, blank=True)
    kapal = models.CharField(max_length=100, null=True, blank=True)
    keretaapian = models.CharField(max_length=200, null=True, blank=True)
    lainnya = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name ="Tingkat"
        verbose_name_plural = "Tingkat"
    
    def __str__(self):
        return f"{self.tingkat}"


class Pegawai(models.Model):
    nip = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=255)
    tgl_lahir = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to="pegawai/foto/", null=True, blank=True)
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE, related_name="pegawais")
    eselon = models.ForeignKey(Eselon, on_delete=models.CASCADE, related_name="pegawais")
    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE, related_name="pegawais")
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE, related_name="pegawais")
    jabatan = models.CharField(max_length=255)
    jenis_jabatan = models.ForeignKey(JenisJabatan, on_delete=models.CASCADE, related_name="pegawais")
    status_asn = models.ForeignKey(StatusASN, on_delete=models.CASCADE, related_name="pegawais")
    tingkat_spd = models.ForeignKey(Tingkat, on_delete=models.CASCADE, related_name="pegawais", null=True, blank=True)
    sub_opd = models.ForeignKey('opd.SubOPD', on_delete=models.CASCADE, related_name="pegawais")

    class Meta:
        verbose_name = "Pegawai"
        verbose_name_plural = "Pegawai"
        
    def __str__(self):
        return f"{self.nama} ({self.nip})"

