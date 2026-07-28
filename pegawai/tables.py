from config.tables import BaseTable, action_column
from .models import Pegawai, Bidang, Eselon, Pangkat, JenisJabatan, StatusASN, Tugas

class PangkatTable(BaseTable):
    aksi = action_column("pangkat_update", "pangkat_delete")

    class Meta(BaseTable.Meta):
        model = Pangkat
        fields = ("no", "pangkat", "golongan", "ruang", "aksi")
        order_by = ("pangkat",)

class BidangTable(BaseTable):
    aksi = action_column("bidang_update", "bidang_delete")

    class Meta(BaseTable.Meta):
        model = Bidang
        fields = ("no", "bidang", "aksi")
        order_by = ("bidang",)

class EselonTable(BaseTable):
    aksi = action_column("eselon_update", "eselon_delete")
    
    class Meta(BaseTable.Meta):
        model = Eselon
        fields = ("no", "eselon", "urutan", "aksi")
        order_by = ("urutan",)

class JenisJabatanTable(BaseTable):
    aksi = action_column("jenis_jabatan_update", "jenis_jabatan_delete")

    class Meta(BaseTable.Meta):
        model = JenisJabatan
        fields = ("no", "nama", "keterangan", "fungsi", "aksi")
        order_by = ("id","nama")

class StatusASNTable(BaseTable):
    aksi = action_column("status_asn_update", "status_asn_delete")

    class Meta(BaseTable.Meta):
        model = StatusASN
        fields = ("no", "nama", "aksi")
        order_by = ("id","nama")

class TugasTable(BaseTable):
    aksi = action_column("tugas_update", "tugas_delete")

    class Meta(BaseTable.Meta):
        model = Tugas
        fields = ("no", "nama", "keterangan", "aksi")
        order_by = ("id","nama")

class PegawaiTable(BaseTable):
    aksi = action_column("pegawai_update", "pegawai_delete")

    class Meta(BaseTable.Meta):
        model = Pegawai
        fields = ("no","nip", "nama", "tgl_lahir","sub_opd","pangkat","eselon","bidang", "aksi")
        order_by = ("eselon","nip")
