from django.contrib import admin

from .models import OPD, SubOPD


@admin.register(OPD)
class OPDAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama")
    search_fields = ("kode", "nama")
    ordering = ("kode",)


@admin.register(SubOPD)
class SubOPDAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama", "opd")
    list_filter = ("opd",)
    search_fields = ("kode", "nama", "opd__nama")
    ordering = ("kode",)
