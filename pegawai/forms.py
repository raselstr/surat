from django import forms
from config.forms import BaseAppModelForm
from .models import Pegawai

class PegawaiForm(BaseAppModelForm):
    class Meta:
        model = Pegawai
        fields = ["nip", "nama", "sub_opd"]
        