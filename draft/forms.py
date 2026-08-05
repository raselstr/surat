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

    field_layout = {
        "tanggalmulai": 3,
        "tanggalselesai": 3,
        "jammulai": 3,
        "jamselesai": 3,
        "tempat": 12,
        "agenda": 12,
        "perlengkapan": 12,
    }

    class Meta:
        model = Undangan
        exclude = ["draft_surat"]

class TujuanSuratForm(BaseAppModelForm):

    field_layout = {
        "instansi": 12,
    }

    class Meta:
        model = TujuanSurat
        exclude = ["draft_surat"]
