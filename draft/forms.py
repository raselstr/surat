from django import forms

from config.forms import BaseAppModelForm
from .models import JenisDokumen, DraftSurat, Undangan, TujuanSurat


class JenisDokumenForm(BaseAppModelForm):
    class Meta:
        model = JenisDokumen
        fields = ["nama"]

class DraftSuratForm(BaseAppModelForm):
    field_layout ={
        "jenis_dokumen": 4,
        "nomor": 2,
        "sifat": 4,
        "lampiran": 4,
        "hal": 4,
        "dari": 4,
        "alamat": 12,
        "pembuka": 12,
        "isi": 12,
        "penutup": 12,
        "tembusan": 6,
        "pejabat_penandatangan":6
    }
    class Meta:
        model = DraftSurat
        fields = ["jenis_dokumen", "nomor", "sifat", "lampiran", "hal", "dari", "alamat", "pembuka", "isi", "penutup", "tembusan", "pejabat_penandatangan"]
        widgets = {
            "nomor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Masukkan nomor surat, misal: 001/UN.01.01/2023"
            }),
            "pembuka": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": (
                    "Masukkan pembuka surat, "
                    "misal: Dengan hormat, Sehubungan dengan ..."
                ),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.normalized_field_layout)
        
class UndanganForm(BaseAppModelForm):
    class Meta:
        model = Undangan
        fields = ["draft_surat", "tanggalmulai", "tanggalselesai", "jammulai", "jamselesai", "tempat", "agenda", "perlengkapan"]

class TujuanSuratForm(BaseAppModelForm):
    class Meta:
        model = TujuanSurat
        fields = ["draft_surat", "instansi"]
