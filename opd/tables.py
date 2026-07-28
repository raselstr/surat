from config.tables import BaseTable, action_column
from .models import OPD, SubOPD, Penandatangan, Pemda, KopSurat


class OPDTable(BaseTable):
    aksi = action_column("opd_update", "opd_delete")

    class Meta(BaseTable.Meta):
        model = OPD
        fields = ("no", "kode", "nama", "aksi")
        order_by = ("kode",)


class SubOPDTable(BaseTable):
    aksi = action_column("subopd_update", "subopd_delete")

    class Meta(BaseTable.Meta):
        model = SubOPD
        fields = ("no", "kode", "nama", "opd", "aksi")
        order_by = ("kode",)

class PenandatanganTable(BaseTable):
    aksi = action_column("penandatangan_update", "penandatangan_delete")

    class Meta(BaseTable.Meta):
        model = Penandatangan
        fields = ("no", "nama", "nip", "pangkat", "tugas", "jabatan", "jenis_jabatan", "opd", "aksi")
        order_by = ("nama",)

class PemdaTable(BaseTable):
    aksi = action_column("pemda_update", "pemda_delete")

    class Meta(BaseTable.Meta):
        model = Pemda
        fields = ("no", "logo", "nama_pemda", "nama_dinas","nama_kabupaten","ibukota", "aksi")
        order_by = ("nama",)

class KopSuratTable(BaseTable):
    aksi = action_column("kopsurat_update", "kopsurat_delete")

    class Meta(BaseTable.Meta):
        model = KopSurat
        fields = ("no", "logo", "nama_pemda", "nama_dinas","nama_kabupaten","ibukota", "aksi")
        order_by = ("nama",)


