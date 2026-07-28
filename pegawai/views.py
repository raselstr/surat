from config.crud.base import FullAccessCRUDView

from .forms import PegawaiForm, BidangForm, EselonForm, PangkatForm, JenisJabatanForm, StatusASNForm, TugasForm
from .models import Pegawai, Bidang, Eselon, Pangkat, JenisJabatan, StatusASN, Tugas
from .tables import PegawaiTable, BidangTable, EselonTable, PangkatTable, JenisJabatanTable, StatusASNTable, TugasTable

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

class JenisJabatanListView(FullAccessCRUDView):
    model = JenisJabatan
    form_class = JenisJabatanForm
    table_class = JenisJabatanTable
    title = "Jenis Jabatan"
    url_list = "/jenis-jabatan/"
    url_action = "/jenis-jabatan/"
    url_action_pk = "/jenis-jabatan/"

class StatusASNListView(FullAccessCRUDView):
    model = StatusASN
    form_class = StatusASNForm
    table_class = StatusASNTable
    title = "Status ASN"
    url_list = "/status-asn/"
    url_action = "/status-asn/"
    url_action_pk = "/status-asn/"

class TugasListView(FullAccessCRUDView):
    model = Tugas
    form_class = TugasForm
    table_class = TugasTable
    title = " Tugas ASN"
    url_list = "/tugas/"
    url_action = "/tugas/"
    url_action_pk = "/tugas/"


class PegawaiListView(FullAccessCRUDView):
    model = Pegawai
    form_class = PegawaiForm
    table_class = PegawaiTable
    title = "Pegawai"
    url_list = "/pegawai/"
    url_action = "/pegawai/"
    url_action_pk = "/pegawai/"
    enable_year_filter = False
