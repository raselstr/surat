from config.crud.base import FullAccessCRUDView

from .forms import PegawaiForm
from .models import Pegawai
from .tables import PegawaiTable

class PegawaiListView(FullAccessCRUDView):
    model = Pegawai
    form_class = PegawaiForm
    table_class = PegawaiTable
    title = "Pegawai"
    url_list = "/pegawai/"
    url_action = "/pegawai/"
    url_action_pk = "/pegawai/"
