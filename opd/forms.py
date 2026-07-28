from django import forms

from config.forms import BaseAppModelForm
from .models import OPD, SubOPD, Penandatangan, Pemda, KopSurat


class OPDForm(BaseAppModelForm):
    class Meta:
        model = OPD
        fields = ["kode", "nama"]


class SubOPDForm(BaseAppModelForm):
    class Meta:
        model = SubOPD
        fields = ["kode", "nama", "opd"]

class PenandatanganForm(BaseAppModelForm):
    class Meta:
        model = Penandatangan
        fields = ["nama", "nip", "pangkat", "tugas", "jabatan", "jenis_jabatan", "subopd"]

class PemdaForm(BaseAppModelForm):
    class Meta:
        model = Pemda
        fields = ["logo", "nama_pemda", "nama_dinas", "nama_kabupaten", "ibukota"]

class KopSuratForm(BaseAppModelForm):
    class Meta:
        model = KopSurat
        fields = [
            "pemda", "default_number_format","font_family", "region_font_size_pt", "office_font_size_pt", 
            "address_font_size_pt","contact_font_size_pt","logo_width_px", "logo_height_px",
            "print_scale_percent","margin_top_mm","margin_bottom_mm","margin_left_mm","margin_right_mm"
            ]
