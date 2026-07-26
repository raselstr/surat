from django import forms

from config.forms import BaseAppModelForm
from .models import OPD, SubOPD


class OPDForm(BaseAppModelForm):
    class Meta:
        model = OPD
        fields = ["kode", "nama"]


class SubOPDForm(BaseAppModelForm):
    class Meta:
        model = SubOPD
        fields = ["kode", "nama", "opd"]
