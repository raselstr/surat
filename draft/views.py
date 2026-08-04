from config.crud.base import FullAccessCRUDView

from .forms import DraftSuratForm, JenisDokumenForm, TujuanSuratForm, UndanganForm
from .models import JenisDokumen, DraftSurat, Undangan, TujuanSurat
from .tables import DraftSuratTable, JenisDokumenTable, TujuanSuratTable, UndanganTable


class JenisDokumenListView(FullAccessCRUDView):
    model = JenisDokumen
    form_class = JenisDokumenForm
    table_class = JenisDokumenTable
    title = "Jenis Dokumen"
    url_list = "/jenis_dokumen/"
    url_action = "/jenis_dokumen/"
    url_action_pk = "/jenis_dokumen/"

class DraftSuratListView(FullAccessCRUDView):
    model = DraftSurat
    form_class = DraftSuratForm
    table_class = DraftSuratTable
    title = "Draft Surat"
    url_list = "/draft_surat/"
    url_action = "/draft_surat/"
    url_action_pk = "/draft_surat/"

class UndanganListView(FullAccessCRUDView):
    model = Undangan
    form_class = UndanganForm
    table_class = UndanganTable
    title = "Undangan"
    url_list = "/undangan/"
    url_action = "/undangan/"
    url_action_pk = "/undangan/"

class TujuanSuratListView(FullAccessCRUDView):
    model = TujuanSurat
    form_class = TujuanSuratForm
    table_class = TujuanSuratTable
    title = "Tujuan Surat"
    url_list = "/tujuan_surat/"
    url_action = "/tujuan_surat/"
    url_action_pk = "/tujuan_surat/"