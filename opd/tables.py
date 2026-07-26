from config.tables import BaseTable, action_column
from .models import OPD, SubOPD


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
