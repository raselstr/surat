from django.db import models
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from config.utils.image_compression import compress_if_image, is_uploaded_image
from django.core.validators import MaxValueValidator, MinValueValidator



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
    opd = models.ForeignKey(OPD, on_delete=models.CASCADE, related_name="subopd")

    class Meta:
        verbose_name = "Sub OPD"
        verbose_name_plural = "Sub OPD"
        ordering = ["kode"]

    def __str__(self):
        return f"{self.nama} ({self.opd.nama})"
    
class Penandatangan(models.Model):
    nama = models.CharField(max_length=200)
    nip = models.CharField(max_length=30, null=True, blank=True)

    pangkat = models.ForeignKey(
        "pegawai.Pangkat",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='penandatangan'
    )

    tugas = models.ForeignKey(
        "pegawai.Tugas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='penandatangan'
    )
    jabatan = models.CharField(max_length=200, null=True, blank=True)

    jenis_jabatan = models.ForeignKey(
        "pegawai.JenisJabatan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='penandatangan'
    )

    subopd = models.ForeignKey(
        SubOPD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='penandatangan'
    )
    
    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['nama', 'tugas','jenis_jabatan', 'subopd'],
                name='uniq_penandatangan_nama_tugas_jenis_jabatan_subopd',
                violation_error_message=(
                    "Penandatangan dengan Nama, tugas, "
                    "jenis jabatan, dan OPD yang sama sudah ada."
                )
            ),   
        ]

    def clean(self):
        super().clean()

        duplicates = Penandatangan.objects.exclude(pk=self.pk).filter(
            nama=self.nama,
            tugas=self.tugas,
            jenis_jabatan=self.jenis_jabatan,
            subopd=self.subopd,
        )

        if not duplicates.exists():
            return

        message = (
            "Penandatangan dengan NIP, nama, tugas, "
            "jenis jabatan, dan OPD yang sama sudah ada."
        )

        raise ValidationError({
            "nip": message,
            "nama": message,
            "tugas": message,
            "jenis_jabatan": message,
            "opd": message,
            NON_FIELD_ERRORS: [message],
        })

    def __str__(self):
        return f"{self.nama} - {self.tugas} - {self.subopd}"

class Pemda(models.Model):
    nama_pemda = models.CharField(max_length=200)
    nama_dinas = models.OneToOneField(
        SubOPD, 
        on_delete=models.PROTECT, 
        null=True, 
        unique=True,
        error_messages={
            'unique': "Nama Dinas sudah digunakan. Pilih nama dinas lain."
        },
        related_name='pemda'
        )
    nama_kabupaten = models.CharField(max_length=200, null=True, blank=True)
    ibukota = models.CharField(max_length=100, null=True, blank=True)
    alamat = models.CharField(max_length=300, null=True, blank=True)
    telepon = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    password_standar = models.CharField(
        max_length=128,
        blank=True,
        default="",
        help_text="Password standar untuk login pegawai dengan NIP.",
    )
    logo = models.ImageField(upload_to='pemda_logos/', null=True, blank=True)

    class Meta:
        ordering = ['nama_pemda']
        verbose_name = 'Pemda'
        verbose_name_plural = 'Pemda'

    def __str__(self):
        return self.nama_pemda

    def save(self, *args, **kwargs):
        if is_uploaded_image(self.logo):
            self.logo = compress_if_image(self.logo, max_edge=1200, quality=90)
        super().save(*args, **kwargs)


class KopSurat(models.Model):
    FONT_FAMILY_CHOICES = [
        ("Arial, sans-serif", "Arial"),
        ('"Times New Roman", Times, serif', "Times New Roman"),
        ("Calibri, Arial, sans-serif", "Calibri"),
        ("Cambria, Georgia, serif", "Cambria"),
        ('Garamond, "Times New Roman", serif', "Garamond"),
        ("Tahoma, Geneva, sans-serif", "Tahoma"),
        ("Verdana, Geneva, sans-serif", "Verdana"),
    ]

    ALIGNMENT_CHOICES = [
        ("left", "Kiri"),
        ("center", "Tengah"),
        ("right", "Kanan"),
    ]

    pemda = models.OneToOneField(
        Pemda,
        on_delete=models.CASCADE,
        related_name="kop_surat",
    )
    font_family = models.CharField(
        max_length=120,
        choices=FONT_FAMILY_CHOICES,
        default="Arial",
        verbose_name="Jenis Font",
    )
    region_font_size_pt = models.PositiveSmallIntegerField(
        default=14,
        validators=[MinValueValidator(8), MaxValueValidator(32)],
        verbose_name="Ukuran Font Nama Pemda (pt)",
    )
    office_font_size_pt = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(8), MaxValueValidator(36)],
        verbose_name="Ukuran Font Nama Dinas/Jabatan (pt)",
    )
    address_font_size_pt = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(8), MaxValueValidator(20)],
        verbose_name="Ukuran Font Alamat (pt)",
    )
    contact_font_size_pt = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(8), MaxValueValidator(20)],
        verbose_name="Ukuran Font Kontak (pt)",
    )
    logo_width_px = models.PositiveSmallIntegerField(
        default=90,
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        verbose_name="Lebar Logo (px)",
    )
    logo_height_px = models.PositiveSmallIntegerField(
        default=90,
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        verbose_name="Tinggi Logo (px)",
    )
    print_scale_percent = models.PositiveSmallIntegerField(
        default=96,
        validators=[MinValueValidator(75), MaxValueValidator(120)],
        verbose_name="Skala Cetak Default (%)",
    )

    # Margin settings for paper edge distance
    margin_top_mm = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="Margin Atas (mm)",
    )
    margin_bottom_mm = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="Margin Bawah (mm)",
    )
    margin_left_mm = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="Margin Kiri (mm)",
    )
    margin_right_mm = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="Margin Kanan (mm)",
    )

    # Default number format for SPT and SPD
    default_number_format = models.CharField(
        max_length=100,
        blank=True,
        default="800.1.11.1/{nomor_urut}/BKAD/{bulan}/{tahun}",
        verbose_name="Format Default Nomor SPT",
        help_text="Gunakan {nomor_urut}, {bulan}, {tahun} sebagai placeholder",
    )
    

    class Meta:
        ordering = ["pemda__nama_pemda"]
        verbose_name = "Kop Surat"
        verbose_name_plural = "Kop Surat"

    @property
    def font_family_css(self):
        return self.font_family or "Arial"

    @property
    def print_scale_decimal(self):
        scale = (self.print_scale_percent or 100) / 100
        return f"{scale:.2f}".rstrip("0").rstrip(".")

    @property
    def margin_css(self):
        return (
            f"{self.margin_top_mm}mm "
            f"{self.margin_right_mm}mm "
            f"{self.margin_bottom_mm}mm "
            f"{self.margin_left_mm}mm"
        )

    def __str__(self):
        return f"Kop Surat - {self.pemda}"