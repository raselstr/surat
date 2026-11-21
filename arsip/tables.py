from config.tables import BaseTable, action_column
from .models import Klasifikasi, Kategori, Unit, Informasi


class KlasifikasiTable(BaseTable):
    aksi = action_column("klasifikasi_update", "klasifikasi_delete")

    class Meta(BaseTable.Meta):
        model = Klasifikasi
        fields = ("no", "kode", "nama", "aksi")
        order_by = ("kode",)


class KategoriTable(BaseTable):
    aksi = action_column("kategori_update", "kategori_delete")

    class Meta(BaseTable.Meta):
        model = Kategori
        fields = ("no", "kode", "nama", "klasifikasi", "aksi")
        order_by = ("kode",)


class UnitTable(BaseTable):
    aksi = action_column("unit_update", "unit_delete")

    class Meta(BaseTable.Meta):
        model = Unit
        fields = ("no", "kode", "nama", "kategori", "aksi")
        order_by = ("kode",)


class InformasiTable(BaseTable):
    aksi = action_column("informasi_update", "informasi_delete")

    class Meta(BaseTable.Meta):
        model = Informasi
        fields = ("no", "kode", "nama", "unit", "aksi")
        order_by = ("kode",)
