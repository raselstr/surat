from config.crud.base import BaseCRUDView

from .forms import OPDForm, SubOPDForm
from .models import OPD, SubOPD
from .tables import OPDTable, SubOPDTable


class OPDListView(BaseCRUDView):
    model = OPD
    form_class = OPDForm
    table_class = OPDTable
    title = "OPD"
    url_list = "/opd/"
    url_action = "/opd/"
    url_action_pk = "/opd/"

    def get_permission(self):
        return type("Perm", (), {"can_view": True, "can_add": True, "can_edit": True, "can_delete": True})()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        context["export_url"] = self.get_export_url()
        context["import_url"] = self.get_import_url()
        return context


class SubOPDListView(BaseCRUDView):
    model = SubOPD
    form_class = SubOPDForm
    table_class = SubOPDTable
    title = "Sub OPD"
    url_list = "/sub-opd/"
    url_action = "/sub-opd/"
    url_action_pk = "/sub-opd/"

    def get_permission(self):
        return type("Perm", (), {"can_view": True, "can_add": True, "can_edit": True, "can_delete": True})()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        context["export_url"] = self.get_export_url()
        context["import_url"] = self.get_import_url()
        return context
