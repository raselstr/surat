from config.crud.base import FullAccessCRUDView

from .forms import PegawaiForm, BidangForm, EselonForm, PangkatForm
from .models import Pegawai, Bidang, Eselon, Pangkat
from .tables import PegawaiTable, BidangTable, EselonTable, PangkatTable

class BidangListView(FullAccessCRUDView):
    model = Bidang
    form_class = BidangForm
    table_class = BidangTable
    title = "Bidang"
    url_list = "/bidang/"
    url_action = "/bidang/"
    url_action_pk = "/bidang/"

class EselonListView(FullAccessCRUDView):
    model = Eselon
    form_class = EselonForm
    table_class = EselonTable
    title = "Eselon"
    url_list = "/eselon/"
    url_action = "/eselon/"
    url_action_pk = "/eselon/"

class PangkatListView(FullAccessCRUDView):
    model = Pangkat
    form_class = PangkatForm
    table_class = PangkatTable
    title = "Pangkat"
    url_list = "/pangkat/"
    url_action = "/pangkat/"
    url_action_pk = "/pangkat/"


class PegawaiListView(FullAccessCRUDView):
    model = Pegawai
    form_class = PegawaiForm
    table_class = PegawaiTable
    title = "Pegawai"
    url_list = "/pegawai/"
    url_action = "/pegawai/"
    url_action_pk = "/pegawai/"