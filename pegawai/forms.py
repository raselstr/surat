from django import forms
from config.forms import BaseAppModelForm
from .models import Pegawai, Bidang, Eselon, Pangkat

class PangkatForm(BaseAppModelForm):
    class Meta:
        model = Pangkat
        fields = ["pangkat", "golongan", "ruang"]

class BidangForm(BaseAppModelForm):
    class Meta:
        model = Bidang
        fields = ["bidang"]

class EselonForm(BaseAppModelForm):
    class Meta:
        model = Eselon
        fields = ["eselon", "urutan"]

class PegawaiForm(BaseAppModelForm):
    class Meta:
        model = Pegawai
        fields = ["nip", "nama", "sub_opd"]

