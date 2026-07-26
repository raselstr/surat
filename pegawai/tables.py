from config.tables import BaseTable, action_column
from .models import Pegawai

class PegawaiTable(BaseTable):
    aksi = action_column("pegawai_update", "pegawai_delete")

    class Meta(BaseTable.Meta):
        model = Pegawai
        fields = ("no", "nip", "nama", "sub_opd", "aksi")
        order_by = ("nip",)