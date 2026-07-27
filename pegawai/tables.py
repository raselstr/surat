from config.tables import BaseTable, action_column
from .models import Pegawai, Bidang, Eselon, Pangkat

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

class PegawaiTable(BaseTable):
    aksi = action_column("pegawai_update", "pegawai_delete")

    class Meta(BaseTable.Meta):
        model = Pegawai
        fields = ("no", "nip", "nama", "sub_opd", "aksi")
        order_by = ("nip",)

