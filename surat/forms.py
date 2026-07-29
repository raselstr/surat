from django import forms

from config.forms import BaseAppModelForm

from .models import (
    DisposisiSurat,
    KlasifikasiSurat,
    LampiranSurat,
    ReviewSurat,
    RiwayatSurat,
    Surat,
    TujuanDisposisi,
)


class KlasifikasiSuratForm(BaseAppModelForm):
    class Meta:
        model = KlasifikasiSurat
        fields = ["kode", "nama", "keterangan"]


class SuratForm(BaseAppModelForm):
    jenis_value = None

    class Meta:
        model = Surat
        fields = [
            "nomor_agenda",
            "nomor_surat",
            "tanggal_surat",
            "tanggal_diterima",
            "tanggal_dikirim",
            "asal_surat",
            "tujuan_surat",
            "perihal",
            "ringkasan",
            "klasifikasi",
            "sifat",
            "unit_pengolah",
            "bidang_pembuat",
            "penanggung_jawab",
        ]
        widgets = {
            "ringkasan": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.jenis_value == Surat.Jenis.MASUK:
            self.fields["tanggal_dikirim"].required = False
        if self.jenis_value == Surat.Jenis.KELUAR:
            self.fields["tanggal_diterima"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.jenis_value:
            instance.jenis = self.jenis_value

        if self.request and self.request.user.is_authenticated:
            if not instance.pk:
                instance.dibuat_oleh = self.request.user
            instance.diperbarui_oleh = self.request.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class SuratMasukForm(SuratForm):
    jenis_value = Surat.Jenis.MASUK


class SuratKeluarForm(SuratForm):
    jenis_value = Surat.Jenis.KELUAR


class ReviewSuratForm(BaseAppModelForm):
    class Meta:
        model = ReviewSurat
        fields = ["surat", "tahap", "keputusan", "catatan", "reviewer"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.request and self.request.user.is_authenticated:
            instance.user = self.request.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class DisposisiSuratForm(BaseAppModelForm):
    class Meta:
        model = DisposisiSurat
        fields = [
            "surat",
            "nomor_disposisi",
            "pemberi",
            "instruksi",
            "catatan",
            "batas_waktu",
            "status",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.request and self.request.user.is_authenticated and not instance.pk:
            instance.dibuat_oleh = self.request.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class TujuanDisposisiForm(BaseAppModelForm):
    class Meta:
        model = TujuanDisposisi
        fields = [
            "disposisi",
            "bidang",
            "penerima",
            "status",
            "catatan_tindak_lanjut",
            "dibaca_pada",
            "selesai_pada",
        ]


class LampiranSuratForm(BaseAppModelForm):
    class Meta:
        model = LampiranSurat
        fields = ["surat", "nama", "berkas", "keterangan"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.request and self.request.user.is_authenticated and not instance.pk:
            instance.diunggah_oleh = self.request.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class RiwayatSuratForm(BaseAppModelForm):
    class Meta:
        model = RiwayatSurat
        fields = [
            "surat",
            "aksi",
            "status_sebelum",
            "status_sesudah",
            "keterangan",
            "user",
        ]


class VerifikasiSuratForm(forms.Form):
    keputusan = forms.ChoiceField(choices=ReviewSurat.Keputusan.choices)
    reviewer = forms.ModelChoiceField(queryset=None, label="Pejabat")
    catatan = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    def __init__(self, *args, **kwargs):
        from pegawai.models import Pegawai

        super().__init__(*args, **kwargs)
        self.fields["reviewer"].queryset = Pegawai.objects.select_related(
            "bidang",
            "tugas",
            "sub_opd",
        )


class DisposisiCepatForm(forms.ModelForm):
    bidang_tujuan = forms.ModelMultipleChoiceField(
        queryset=None,
        label="Bidang Tujuan",
        widget=forms.SelectMultiple(attrs={"class": "form-select select2"}),
    )

    class Meta:
        model = DisposisiSurat
        fields = [
            "nomor_disposisi",
            "pemberi",
            "instruksi",
            "catatan",
            "batas_waktu",
            "bidang_tujuan",
        ]

    def __init__(self, *args, **kwargs):
        from pegawai.models import Bidang

        self.request = kwargs.pop("request", None)
        self.surat = kwargs.pop("surat")
        super().__init__(*args, **kwargs)
        self.fields["bidang_tujuan"].queryset = Bidang.objects.order_by("bidang")

        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("class", "form-control")
                field.widget.attrs.setdefault("rows", 3)
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.setdefault("class", "form-select select2")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select select2")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    def save(self, commit=True):
        disposisi = super().save(commit=False)
        disposisi.surat = self.surat
        disposisi.status = DisposisiSurat.Status.DIKIRIM

        if self.request and self.request.user.is_authenticated:
            disposisi.dibuat_oleh = self.request.user

        if commit:
            disposisi.save()
            for bidang in self.cleaned_data["bidang_tujuan"]:
                TujuanDisposisi.objects.create(disposisi=disposisi, bidang=bidang)

        return disposisi
