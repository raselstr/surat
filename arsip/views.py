from config.crud.base import FullAccessCRUDView

from .forms import InformasiForm, KategoriForm, KlasifikasiForm, UnitForm
from .models import Informasi, Kategori, Klasifikasi, Unit
from .tables import InformasiTable, KategoriTable, KlasifikasiTable,UnitTable


class KlasifikasiListView(FullAccessCRUDView):
    model = Klasifikasi
    form_class = KlasifikasiForm
    table_class = KlasifikasiTable
    title = "Klasifikasi"
    url_list = "/klasifikasi/"
    url_action = "/klasifikasi/"
    url_action_pk = "/klasifikasi/"

class KategoriListView(FullAccessCRUDView):
    model = Kategori
    form_class = KategoriForm
    table_class = KategoriTable
    title = "Kategori"
    url_list = "/kategori/"
    url_action = "/kategori/"
    url_action_pk = "/kategori/"

class UnitListView(FullAccessCRUDView):
    model = Unit
    form_class = UnitForm
    table_class = UnitTable
    title = "Unit"
    url_list = "/unit/"
    url_action = "/unit/"
    url_action_pk = "/unit/"

class InformasiListView(FullAccessCRUDView):
    model = Informasi
    form_class = InformasiForm
    table_class = InformasiTable
    title = "Informasi"
    url_list = "/informasi/"
    url_action = "/informasi/"
    url_action_pk = "/informasi/"