import json

from django.contrib import messages
from django.db import models, transaction
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django_tables2 import RequestConfig
from types import SimpleNamespace
from config.views_excel import ExcelMixin
from config.utils.formatting import is_money_identifier, parse_localized_decimal


class BaseCRUDView(ExcelMixin, ListView):
    model = None
    form_class = None
    table_class = None
    template_name = "components/crud/list.html"
    template_list = "components/crud/list.html"
    template_form = "components/crud/form_general.html"
    template_form_page = "components/crud/form_page.html"
    template_delete = "components/crud/delete.html"
    template_delete_page = "components/crud/delete_page.html"

    title = ""

    url_list = None
    url_action = None
    url_action_pk = None
    url_import = None
    url_export = None
    paginate_by = None
    use_crud_modal = True
    use_excel_modal = True
    enable_year_filter = True

    # =========================
    # 🔥 PERMISSION
    # =========================
    def get_permission(self):
        from menus.models import RolePermission, SubMenu

        user = self.request.user

        if not user.is_authenticated:
            return None

        if user.is_superuser:
            return SimpleNamespace(
                can_view=True,
                can_add=True,
                can_edit=True,
                can_delete=True
            )

        profile = getattr(user, "userprofile", None)
        if not profile or not getattr(profile, "role_id", None):
            return None

        resolver_match = getattr(self.request, "resolver_match", None)
        url_name = getattr(resolver_match, "url_name", "") or ""
        for suffix in ("_add", "_update", "_delete"):
            if url_name.endswith(suffix):
                url_name = f"{url_name[:-len(suffix)]}_list"

        try:
            submenu = SubMenu.objects.get(url_name=url_name)
        except SubMenu.DoesNotExist:
            return None

        return RolePermission.objects.filter(
            role=profile.role,
            submenu=submenu
        ).first()

    # 🔥 helper biar konsisten (HTMX vs normal)
    def _forbidden(self, request):
        if request.headers.get("HX-Request"):
            response = render(request, "components/crud/403.html", status=403)
            response["HX-Retarget"] = "#modal-body"
            response["HX-Reswap"] = "innerHTML"
            return response
        return render(request, "components/crud/403.html", status=403)

    def _get_success_notification(self, action):
        action_labels = {
            "add": "ditambahkan",
            "update": "diperbarui",
            "delete": "dihapus",
        }
        model_name = self.model._meta.verbose_name

        return {
            "title": "Berhasil",
            "message": f"Data {model_name} berhasil {action_labels[action]}.",
            "level": "success",
            "action": action,
        }

    def _add_success_message(self, request, action):
        notification = self._get_success_notification(action)
        messages.success(request, notification["message"])

    def _build_htmx_success_response(self, action):
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({
            "crudSuccess": self._get_success_notification(action),
        })
        return response

    def _collect_form_errors(self, form, formset=None):
        errors = []

        if form.non_field_errors():
            errors.extend(str(error) for error in form.non_field_errors())

        for field in form:
            for error in field.errors:
                errors.append(f"{field.label}: {error}")

        if formset is not None:
            if formset.non_form_errors():
                errors.extend(str(error) for error in formset.non_form_errors())

            for index, child_form in enumerate(formset.forms, start=1):
                if child_form.non_field_errors():
                    errors.extend(
                        f"Pelaksana {index}: {error}"
                        for error in child_form.non_field_errors()
                    )

                for field in child_form.visible_fields():
                    for error in field.errors:
                        errors.append(
                            f"Pelaksana {index} - {field.label}: {error}"
                        )

        return errors

    def _build_htmx_error_response(self, request, context, form, formset=None):
        response = render(request, self.template_form, context)
        errors = self._collect_form_errors(form, formset)

        response["HX-Trigger"] = json.dumps({
            "crudError": {
                "title": "Validasi gagal",
                "message": (
                    errors[0]
                    if errors else "Periksa kembali data yang diinput."
                ),
                "level": "error",
            },
        })
        return response

    # =========================
    def get_base_queryset(self):
        return self.model.objects.all().order_by('id')

    def get_object_queryset(self):
        return self.get_base_queryset()

    def get_form_kwargs(self, request, instance=None):
        kwargs = {
            "data": request.POST or None,
            "files": request.FILES or None,
            "instance": instance,
        }

        if getattr(self.form_class, "accepts_request", False):
            kwargs["request"] = request

        return kwargs

    def get_formset_kwargs(self, request, instance=None):
        kwargs = {
            "data": request.POST or None,
            "files": request.FILES or None,
            "instance": instance,
        }

        if getattr(self.formset_class.form, "accepts_request", False):
            kwargs["form_kwargs"] = {"request": request}

        return kwargs

    def get_queryset(self):
        qs = self.get_base_queryset()
        qs = self.apply_active_year_filter(qs)
        search = self.request.GET.get("search")

        if not search:
            return qs

        model_fields = {
            field.name: field
            for field in self.model._meta.get_fields()
            if getattr(field, "name", None)
        }
        field_names = set(model_fields.keys())
        filters = Q()

        def is_relation(field_name):
            return getattr(model_fields.get(field_name), "is_relation", False)

        def add_text_filter(field_name, related_lookup=None):
            nonlocal filters

            if field_name not in field_names:
                return

            if is_relation(field_name):
                if related_lookup:
                    filters |= Q(**{related_lookup: search})
                return

            filters |= Q(**{f"{field_name}__icontains": search})

        if 'nama' in field_names:
            filters |= Q(nama__icontains=search)
        if 'nip' in field_names:
            filters |= Q(nip__icontains=search)
        if 'jabatan' in field_names:
            filters |= Q(jabatan__icontains=search)
        add_text_filter('pangkat', 'pangkat__pangkat__icontains')
        add_text_filter('eselon', 'eselon__eselon__icontains')
        add_text_filter('jenis_jabatan', 'jenis_jabatan__nama__icontains')
        add_text_filter('status', 'status__nama__icontains')
        add_text_filter('opd', 'opd__nama__icontains')
        add_text_filter('tingkat', 'tingkat__tingkat__icontains')
        if 'tugas' in field_names:
            filters |= Q(tugas__icontains=search)
        if 'nama_pemda' in field_names:
            filters |= Q(nama_pemda__icontains=search)
        if 'nama_dinas' in field_names:
            filters |= Q(nama_dinas__icontains=search)
        if 'alamat' in field_names:
            filters |= Q(alamat__icontains=search)
        if 'telepon' in field_names:
            filters |= Q(telepon__icontains=search)
        if 'email' in field_names:
            filters |= Q(email__icontains=search)
        if 'username' in field_names:
            filters |= Q(username__icontains=search)
        if 'first_name' in field_names:
            filters |= Q(first_name__icontains=search)
        if 'last_name' in field_names:
            filters |= Q(last_name__icontains=search)
        add_text_filter('pemda', 'pemda__nama_pemda__icontains')
        if 'font_family' in field_names:
            filters |= Q(font_family__icontains=search)
        if 'nomor_spt' in field_names:
            filters |= Q(nomor_spt__icontains=search)
        if 'url' in field_names:
            filters |= Q(url__icontains=search)
        add_text_filter('menu', 'menu__nama__icontains')
        if 'icon' in field_names:
            filters |= Q(icon__icontains=search)
        add_text_filter('lokasi', 'lokasi__lokasi__icontains')
        if 'kota' in field_names:
            filters |= Q(kota__icontains=search)
        add_text_filter('jenis_spd', 'jenis_spd__nama__icontains')
        add_text_filter('jenis_kegiatan', 'jenis_kegiatan__nama__icontains')
        add_text_filter('jenis_transportasi', 'jenis_transportasi__nama__icontains')
        add_text_filter('penandatangan', 'penandatangan__nama__icontains')
        if 'spt' in field_names and is_relation('spt'):
            filters |= (
                Q(spt__tempat_tujuan__icontains=search) |
                Q(spt__kota_tujuan__lokasi__icontains=search)
            )
        money_field_types = (
            models.DecimalField,
            models.FloatField,
            models.IntegerField,
            models.BigIntegerField,
            models.PositiveBigIntegerField,
            models.PositiveIntegerField,
            models.PositiveSmallIntegerField,
            models.SmallIntegerField,
        )
        money_field_names = [
            field.name
            for field in self.model._meta.fields
            if isinstance(field, money_field_types) and is_money_identifier(field.name)
        ]

        if money_field_names:
            try:
                money_value = parse_localized_decimal(search)
                for field_name in money_field_names:
                    filters |= Q(**{field_name: money_value})
            except (TypeError, ValueError):
                pass
        

        if filters:
            qs = qs.filter(filters)

        return qs

    def get_active_year(self):
        year = self.request.session.get("active_year") or timezone.localdate().year

        try:
            return int(year)
        except (TypeError, ValueError):
            return timezone.localdate().year

    def get_year_filter_field(self):
        if not self.enable_year_filter:
            return None

        concrete_fields = [
            field
            for field in self.model._meta.get_fields()
            if getattr(field, "concrete", False)
        ]

        for field in concrete_fields:
            if field.name == "tahun":
                return field

        for field in concrete_fields:
            if isinstance(field, (models.DateField, models.DateTimeField)):
                return field

        return None

    def apply_active_year_filter(self, qs):
        field = self.get_year_filter_field()

        if field is None:
            return qs

        active_year = self.get_active_year()

        if field.name == "tahun":
            return qs.filter(tahun=active_year)

        return qs.filter(**{f"{field.name}__year": active_year})

    def get_table_class(self):
        return self.table_class

    def get_table_queryset(self, queryset=None):
        if queryset is not None:
            return queryset
        return self.get_queryset()

    def get_table_kwargs(self, queryset):
        return {"request": self.request}

    def get_table_extra_context(self, queryset):
        return {
            "url_list": self.url_list,
            "use_crud_modal": self.use_crud_modal,
        }

    def get_table(self, queryset=None):
        table_class = self.get_table_class()
        resolved_queryset = self.get_table_queryset(queryset)
        table = table_class(resolved_queryset, **self.get_table_kwargs(resolved_queryset))

        extra_context = self.get_table_extra_context(resolved_queryset)
        existing_extra_context = getattr(table, "extra_context", None) or {}
        table.extra_context = {**existing_extra_context, **extra_context}

        return table

    def get_form(self, request, instance=None):
        return self.form_class(**self.get_form_kwargs(request, instance=instance))

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, request, instance=None):
        formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs(request, instance=instance))

    def get_success_redirect_url(self):
        return self.url_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()  # Don't convert to list - use QuerySet for pagination

        table = self.get_table(qs)

        per_page = self.request.GET.get("per_page", 10)
        normalized_per_page = 25 if per_page == "all" else per_page

        try:
            paginate_config = {
                "per_page": int(normalized_per_page),
                "silent": True,
            }
        except ValueError:
            paginate_config = {
                "per_page": 10,
                "silent": True,
            }

        RequestConfig(self.request, paginate=paginate_config).configure(table)

        context.update({
            "permission": self.get_permission(),
            "table": table,
            "title": self.title,
            "url_list": self.url_list,
            "url_action": self.url_action,
            "url_action_pk": self.url_action_pk,
            "url_import": self.url_import,
            "url_export": self.url_export,
            "initial_url": self.url_list,
            "use_crud_modal": self.use_crud_modal,
            "use_excel_modal": self.use_excel_modal,
            "active_year": self.get_active_year(),
            "has_year_filter": self.get_year_filter_field() is not None,
        })

        return context

    def get_form_template_name(self, request):
        if request.headers.get("HX-Request"):
            return self.template_form
        return self.template_form_page

    def get_delete_template_name(self, request):
        if request.headers.get("HX-Request"):
            return self.template_delete
        return self.template_delete_page

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return [self.template_list]
        return [self.template_name]

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        path_parts = [part for part in request.path.strip("/").split("/") if part]
        url_name = getattr(getattr(request, "resolver_match", None), "url_name", "") or ""

        if pk and "delete" in request.path:
            return self.delete_view(request, pk)

        if pk and "form" in request.path:
            return self.form_view(request, pk)

        if "form" in path_parts or url_name.endswith("_add") or (path_parts and path_parts[-1] == "add"):
            return self.form_view(request)

        return super().dispatch(request, *args, **kwargs)

    def list_view(self, request):
        qs = self.get_queryset()
        table = self.get_table(qs)

        return render(request, self.template_list, {
            "table": table,
            "url_list": self.url_list,
        })

    # =========================
    # CREATE / UPDATE
    # =========================
    def form_view(self, request, pk=None):
        perm = self.get_permission()

        # 🔥 PERMISSION CHECK
        if pk:
            if not perm or not perm.can_edit:
                return self._forbidden(request)
        else:
            if not perm or not perm.can_add:
                return self._forbidden(request)

        instance = None
        if pk:
            instance = get_object_or_404(
                self.get_object_queryset(),
                pk=pk,
            )

        form = self.get_form(request, instance=instance)

        if request.method == "POST" and form.is_valid():
            action = "update" if instance else "add"
            form.save()

            if request.headers.get("HX-Request"):
                return self._build_htmx_success_response(action)

            self._add_success_message(request, action)
            return redirect(self.get_success_redirect_url())

        context = {
            "form": form,
            "title": self.title,
            "permission": perm,
            "url_list": self.url_list,
            "form_action": request.path,
            "submit_label": "Simpan Perubahan" if instance else "Simpan Data",
            "is_multipart_form": form.is_multipart(),
            "use_modal": request.headers.get("HX-Request"),
            "template_form": self.template_form,
        }

        if request.method == "POST" and request.headers.get("HX-Request"):
            return self._build_htmx_error_response(
                request,
                context,
                form,
            )

        return render(request, self.get_form_template_name(request), context)

    # =========================
    # DELETE
    # =========================
    def delete_view(self, request, pk):
        perm = self.get_permission()

        if not perm or not perm.can_delete:
            return self._forbidden(request)

        obj = get_object_or_404(
            self.get_object_queryset(),
            pk=pk,
        )

        if request.method == "POST":
            obj.delete()

            if request.headers.get("HX-Request"):
                return self._build_htmx_success_response("delete")

            self._add_success_message(request, "delete")
            return redirect(self.get_success_redirect_url())

        return render(request, self.get_delete_template_name(request), {
            "object": obj,
            "url_list": self.url_list,
            "title": "Hapus Data",
            "delete_action": request.path,
            "use_modal": request.headers.get("HX-Request"),
        })

class BaseMasterDetailCRUDView(BaseCRUDView):
    """
    Base CRUD untuk Parent + Child (Master Detail)

    Contoh:
    - SPT + Pelaksana
    - SPD + Rincian
    - Invoice + Items
    - Surat + Lampiran
    """

    # khusus override template form saja
    template_form = "components/crud/form_master_detail.html"

    # wajib diisi di child view
    formset_class = None

    def form_view(self, request, pk=None):
        perm = self.get_permission()

        # =========================
        # Permission Check
        # =========================
        if pk:
            if not perm or not perm.can_edit:
                return self._forbidden(request)
        else:
            if not perm or not perm.can_add:
                return self._forbidden(request)

        # =========================
        # Ambil instance parent
        # =========================
        instance = None
        if pk:
            instance = get_object_or_404(
                self.get_object_queryset(),
                pk=pk
            )

        # safety check
        if not self.formset_class:
            raise ValueError(
                "formset_class harus diisi pada BaseMasterDetailCRUDView"
            )

        # =========================
        # Parent Form
        # =========================
        form = self.get_form(request, instance=instance)

        # =========================
        # Child Formset
        # =========================
        formset = self.get_formset(request, instance=instance)

        # =========================
        # SAVE
        # =========================
        if request.method == "POST":
            if form.is_valid() and formset.is_valid():
                with transaction.atomic():
                    # simpan parent dulu
                    parent = form.save()

                    # kaitkan child ke parent
                    formset.instance = parent
                    formset.save()

                action = "update" if instance else "add"

                # HTMX response
                if request.headers.get("HX-Request"):
                    return self._build_htmx_success_response(action)

                # normal response
                self._add_success_message(request, action)
                return redirect(self.get_success_redirect_url())

        # =========================
        # Render Form
        # =========================
        context = {
            "form": form,
            "formset": formset,
            "title": self.title,
            "permission": perm,
            "url_list": self.url_list,
            "is_multipart_form": (
                form.is_multipart() or formset.is_multipart()
            ),
            "form_action": request.path,
            "submit_label": "Simpan Perubahan" if instance else "Simpan Data",
            "use_modal": request.headers.get("HX-Request"),
            "template_form": self.template_form,
        }

        if request.method == "POST" and request.headers.get("HX-Request"):
            return self._build_htmx_error_response(
                request,
                context,
                form,
                formset=formset,
            )

        return render(request, self.get_form_template_name(request), context)

class FullAccessCRUDView(BaseCRUDView):
    def get_permission(self):
        return SimpleNamespace(can_view=True, can_add=True, can_edit=True, can_delete=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        return context
