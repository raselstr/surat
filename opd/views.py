from config.crud.base import FullAccessCRUDView

from .forms import OPDForm, SubOPDForm, PenandatanganForm, PemdaForm, KopSuratForm
from .models import OPD, SubOPD, Penandatangan, Pemda, KopSurat
from .tables import OPDTable, SubOPDTable, PenandatanganTable, PemdaTable, KopSuratTable


class OPDListView(FullAccessCRUDView):
    model = OPD
    form_class = OPDForm
    table_class = OPDTable
    title = "OPD"
    url_list = "/opd/"
    url_action = "/opd/"
    url_action_pk = "/opd/"

class SubOPDListView(FullAccessCRUDView):
    model = SubOPD
    form_class = SubOPDForm
    table_class = SubOPDTable
    title = "Sub OPD"
    url_list = "/sub-opd/"
    url_action = "/sub-opd/"
    url_action_pk = "/sub-opd/"

class PenandatanganListView(FullAccessCRUDView):
    model = Penandatangan
    form_class = PenandatanganForm
    table_class = PenandatanganTable
    title = "Penandatangan"
    url_list = "/penandatangan/"
    url_action = "/penandatangan/"
    url_action_pk = "/penandatangan/"

class PemdaListView(FullAccessCRUDView):
    model = Pemda
    form_class = PemdaForm
    table_class = PemdaTable
    title = "Pemda"
    url_list = "/pemda/"
    url_action = "/pemda/"
    url_action_pk = "/pemda/"

class KopSuratListView(FullAccessCRUDView):
    model = KopSurat
    form_class = KopSuratForm
    table_class = KopSuratTable
    title = "Kop Surat"
    url_list = "/kop-surat/"
    url_action = "/kop-surat/"
    url_action_pk = "/kop-surat/"
