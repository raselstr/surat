from django.urls import path

from .views import OPDListView, SubOPDListView

urlpatterns = [
    path("opd/", OPDListView.as_view(), name="opd_list"),
    path("opd/add/", OPDListView.as_view(), name="opd_add"),
    path("opd/<int:pk>/form/", OPDListView.as_view(), name="opd_update"),
    path("opd/<int:pk>/delete/", OPDListView.as_view(), name="opd_delete"),

    path("sub-opd/", SubOPDListView.as_view(), name="subopd_list"),
    path("sub-opd/add/", SubOPDListView.as_view(), name="subopd_add"),
    path("sub-opd/<int:pk>/form/", SubOPDListView.as_view(), name="subopd_update"),
    path("sub-opd/<int:pk>/delete/", SubOPDListView.as_view(), name="subopd_delete"),
]
