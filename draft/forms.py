from django import forms

from config.forms import BaseAppModelForm
from .models import JenisDokumen, DraftSurat, Undangan, TujuanSurat


class JenisDokumenForm(BaseAppModelForm):
    class Meta:
        model = JenisDokumen
        fields = ["nama"]

class DraftSuratForm(BaseAppModelForm):
    field_layout ={
        "jenis_dokumen": 3,
        "nomor": 3,
        "sifat": 3,
        "lampiran": 3,
        "hal": 12,
        "dari": 8,
        "alamat": 4,
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
            "dari": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "isi jika akan membuat Nota Dinas"
            }),
            "alamat": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kosongkan jika tidak ada"
            }),
        }
class UndanganForm(BaseAppModelForm):
    class Meta:
        model = Undangan
        fields = ["draft_surat", "tanggalmulai", "tanggalselesai", "jammulai", "jamselesai", "tempat", "agenda", "perlengkapan"]

class TujuanSuratForm(BaseAppModelForm):
    class Meta:
        model = TujuanSurat
        fields = ["draft_surat", "instansi"]
