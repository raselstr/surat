from django.urls import path
from .views_excel import GenericExcelExportView, GenericExcelImportView

app_name = 'config'

urlpatterns = [
    # Generic Excel export/import
    path('excel/<str:app_label>/<str:model_name>/export/', GenericExcelExportView.as_view(), name='generic_excel_export'),
    path('excel/<str:app_label>/<str:model_name>/import/', GenericExcelImportView.as_view(), name='generic_excel_import'),
]