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

    def get_search_relation_depth(self):
        return 2

    def is_searchable_text_field(self, field):
        return isinstance(
            field,
            (
                models.CharField,
                models.TextField,
                models.EmailField,
                models.URLField,
                models.SlugField,
            ),
        )

    def get_searchable_lookups(self, model=None, prefix="", depth=None, seen=None):
        model = model or self.model
        depth = self.get_search_relation_depth() if depth is None else depth
        seen = set() if seen is None else seen
        lookups = []

        if model in seen:
            return lookups

        seen.add(model)

        for field in model._meta.get_fields():
            if not getattr(field, "concrete", False):
                continue

            if self.is_searchable_text_field(field):
                lookups.append(f"{prefix}{field.name}__icontains")
                continue

            if depth <= 0:
                continue

            if not isinstance(field, (models.ForeignKey, models.OneToOneField)):
                continue

            related_model = getattr(field.remote_field, "model", None)
            if related_model is None or isinstance(related_model, str):
                continue

            lookups.extend(
                self.get_searchable_lookups(
                    model=related_model,
                    prefix=f"{prefix}{field.name}__",
                    depth=depth - 1,
                    seen=seen.copy(),
                )
            )

        return lookups

    def build_search_filter(self, search):
        filters = Q()

        for lookup in self.get_searchable_lookups():
            filters |= Q(**{lookup: search})

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

        return filters

    def get_queryset(self):
        qs = self.get_base_queryset()
        qs = self.apply_active_year_filter(qs)
        search = self.request.GET.get("search")

        if not search:
            return qs

        filters = self.build_search_filter(search)

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

class BaseOneToOneCRUDView(BaseCRUDView):
    """
    CRUD untuk Parent dengan beberapa relasi OneToOne.

    Contoh:
        DraftSurat
            ├── TujuanSurat
            └── Undangan
    """

    extra_forms = {}

    def get_extra_forms(self, request, instance=None):
        forms = {}

        for related_name, form_class in self.extra_forms.items():

            related_instance = None

            if instance:
                try:
                    related_instance = getattr(instance, related_name)
                except Exception:
                    related_instance = None

            kwargs = {
                "data": request.POST or None,
                "files": request.FILES or None,
                "instance": related_instance,
            }

            if getattr(form_class, "accepts_request", False):
                kwargs["request"] = request

            forms[related_name] = form_class(**kwargs)

        return forms

    def form_view(self, request, pk=None):

        perm = self.get_permission()

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
        extra_forms = self.get_extra_forms(request, instance)

        if request.method == "POST":

            valid = form.is_valid()

            for child_form in extra_forms.values():
                valid = valid and child_form.is_valid()

            if valid:

                with transaction.atomic():

                    parent = form.save()

                    for child_form in extra_forms.values():

                        child = child_form.save(commit=False)

                        linked = False

                        for field in child._meta.fields:

                            if isinstance(field, (models.OneToOneField, models.ForeignKey)):
                                if field.related_model == parent.__class__:
                                    setattr(child, field.name, parent)
                                    linked = True
                                    break

                        if not linked:
                            raise ValueError(
                                f"Tidak ditemukan relasi ke {parent.__class__.__name__}"
                            )

                        child.save()

                action = "update" if instance else "add"

                if request.headers.get("HX-Request"):
                    return self._build_htmx_success_response(action)

                self._add_success_message(request, action)

                return redirect(
                    self.get_success_redirect_url()
                )

        context = {
            "form": form,
            "extra_forms": [
                (
                    related_name.replace("_", " ").title(),
                    frm,
                )
                for related_name, frm in extra_forms.items()
            ],
            "title": self.title,
            "permission": perm,
            "url_list": self.url_list,
            "form_action": request.path,
            "submit_label": (
                "Simpan Perubahan"
                if instance else
                "Simpan Data"
            ),
            "is_multipart_form": any(
                f.is_multipart()
                for f in [form, *extra_forms.values()]
            ),
            "use_modal": request.headers.get("HX-Request"),
            "template_form": self.template_form,
        }

        if request.method == "POST" and request.headers.get("HX-Request"):
            return self._build_htmx_error_response(
                request,
                context,
                form,
            )

        return render(
            request,
            self.get_form_template_name(request),
            context,
        )
class FullAccessCRUDView(BaseCRUDView):
    def get_permission(self):
        return SimpleNamespace(can_view=True, can_add=True, can_edit=True, can_delete=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        return context

class BaseMultiFormCRUDView(BaseCRUDView):
    extra_forms = {}

    def get_extra_forms(self, request, instance=None):
        forms = {}

        for name, form_class in self.extra_forms.items():
            forms[name] = form_class(
                data=request.POST or None,
                files=request.FILES or None,
            )

        return forms