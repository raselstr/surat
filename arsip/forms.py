from django import forms

from config.forms import BaseAppModelForm
from .models import Klasifikasi, Kategori, Unit, Informasi


class KlasifikasiForm(BaseAppModelForm):
    class Meta:
        model = Klasifikasi
        fields = ["kode", "nama"]


class KategoriForm(BaseAppModelForm):
    class Meta:
        model = Kategori
        fields = ["klasifikasi", "kode", "nama"]


class UnitForm(BaseAppModelForm):
    class Meta:
        model = Unit
        fields = ["kategori", "kode", "nama"]


class InformasiForm(BaseAppModelForm):
    class Meta:
        model = Informasi
        fields = ["unit", "kode", "nama"]
