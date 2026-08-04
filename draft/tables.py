from config.tables import BaseTable, action_column
from .models import JenisDokumen, DraftSurat, Undangan, TujuanSurat


class JenisDokumenTable(BaseTable):
    aksi = action_column("jenis_dokumen_update", "jenis_dokumen_delete")

    class Meta(BaseTable.Meta):
        model = JenisDokumen
        fields = ("no", "nama", "aksi")
        order_by = ("nama",)

class DraftSuratTable(BaseTable):
    aksi = action_column("draft_surat_update", "draft_surat_delete")

    class Meta(BaseTable.Meta):
        model = DraftSurat
        fields = ("no", "jenis_dokumen", "nomor", "sifat", "lampiran", "hal", "dari", "alamat", "pembuka", "isi", "penutup", "tembusan", "pejabat_penandatangan", "aksi")
        order_by = ("jenis_dokumen",)

class UndanganTable(BaseTable):
    aksi = action_column("undangan_update", "undangan_delete")

    class Meta(BaseTable.Meta):
        model = Undangan
        fields = ("no", "draft_surat", "tanggalmulai", "tanggalselesai", "jammulai", "jamselesai", "tempat", "agenda", "perlengkapan", "aksi")
        order_by = ("tanggalmulai",)

class TujuanSuratTable(BaseTable):
    aksi = action_column("tujuan_surat_update", "tujuan_surat_delete")

    class Meta(BaseTable.Meta):
        model = TujuanSurat
        fields = ("no", "draft_surat", "instansi", "aksi")
        order_by = ("instansi",)