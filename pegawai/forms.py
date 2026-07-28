from django import forms
from config.forms import BaseAppModelForm
from .models import Pegawai, Bidang, Eselon, Pangkat, JenisJabatan, StatusASN, Tugas

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

class JenisJabatanForm(BaseAppModelForm):
    class Meta:
        model = JenisJabatan
        fields = ["nama", "keterangan", "fungsi"]

class StatusASNForm(BaseAppModelForm):
    class Meta:
        model = StatusASN
        fields = ["nama"]

class TugasForm(BaseAppModelForm):
    class Meta:
        model = Tugas
        fields = ["nama", "keterangan"]

class PegawaiForm(BaseAppModelForm):
    class Meta:
        model = Pegawai
        fields = ["nip", "nama", "pangkat","eselon","bidang","tugas","jabatan","jenis_jabatan","status_asn","sub_opd"]
