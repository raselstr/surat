from types import SimpleNamespace

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from config.crud.base import FullAccessCRUDView, BaseCRUDView

from .forms import MenuForm, RoleForm, SubMenuForm, UserForm
from .models import Menu, Role, RolePermission, SubMenu
from .tables import MenuTable, RoleTable, SubMenuTable, UserTable


User = get_user_model()

class MenuListView(FullAccessCRUDView):
    model = Menu
    form_class = MenuForm
    table_class = MenuTable
    title = "Menu"
    url_list = "/menu/"
    url_action = "/menu/"
    url_action_pk = "/menu/"


class SubMenuListView(FullAccessCRUDView):
    model = SubMenu
    form_class = SubMenuForm
    table_class = SubMenuTable
    title = "Sub Menu"
    url_list = "/sub-menu/"
    url_action = "/sub-menu/"
    url_action_pk = "/sub-menu/"


class RoleListView(FullAccessCRUDView):
    model = Role
    form_class = RoleForm
    table_class = RoleTable
    title = "Role"
    url_list = "/role/"
    url_action = "/role/"
    url_action_pk = "/role/"


class UserListView(BaseCRUDView):
    model = User
    form_class = UserForm
    table_class = UserTable
    title = "User"
    url_list = "/user/"
    url_action = "/user/"
    url_action_pk = "/user/"
    enable_excel = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self._forbidden(request)

        return super().dispatch(request, *args, **kwargs)

    def get_permission(self):
        return SimpleNamespace(can_view=True, can_add=True, can_edit=True, can_delete=True)

    def get_base_queryset(self):
        return self.model.objects.select_related("userprofile__role").all().order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        return context

    def delete_view(self, request, pk):
        if str(request.user.pk) == str(pk):
            messages.error(request, "User yang sedang login tidak bisa dihapus.")
            return redirect(self.url_list)

        return super().delete_view(request, pk)


class RolePermissionListView(FullAccessCRUDView):
    model = RolePermission
    form_class = None
    table_class = None
    template_name = "menus/role_permission_list.html"
    title = "Hak Akses Menu"
    url_list = "/hak-akses-menu/"
    url_action = "/hak-akses-menu/"
    url_action_pk = "/hak-akses-menu/"

    def _get_selected_role(self):
        role_id = self.request.POST.get("role") or self.request.GET.get("role")
        roles = Role.objects.all()

        if role_id:
            return roles.filter(pk=role_id).first()

        return roles.first()

    def _build_permission_groups(self, role):
        existing_permissions = {
            permission.submenu_id: permission
            for permission in RolePermission.objects.filter(role=role)
        }

        groups = []
        menus = Menu.objects.filter(aktif=True).prefetch_related("submenus")

        for menu in menus:
            submenu_items = []
            for submenu in menu.submenus.filter(aktif=True):
                permission = existing_permissions.get(submenu.pk)
                if permission is None:
                    permission = RolePermission(role=role, submenu=submenu)

                submenu_items.append({
                    "submenu": submenu,
                    "permission": permission,
                })

            if submenu_items:
                groups.append({
                    "menu": menu,
                    "submenus": submenu_items,
                })

        return groups

    def get_context_data(self, **kwargs):
        context = super(BaseCRUDView, self).get_context_data(**kwargs)
        selected_role = self._get_selected_role()

        context.update({
            "title": self.title,
            "roles": Role.objects.all(),
            "selected_role": selected_role,
            "permission_groups": (
                self._build_permission_groups(selected_role)
                if selected_role else []
            ),
            "url_list": self.url_list,
        })
        return context

    def post(self, request, *args, **kwargs):
        selected_role = self._get_selected_role()
        if not selected_role:
            messages.error(request, "Role belum tersedia.")
            return redirect(self.url_list)

        submenus = SubMenu.objects.filter(aktif=True)
        for submenu in submenus:
            RolePermission.objects.update_or_create(
                role=selected_role,
                submenu=submenu,
                defaults={
                    "can_view": f"can_view_{submenu.pk}" in request.POST,
                    "can_add": f"can_add_{submenu.pk}" in request.POST,
                    "can_edit": f"can_edit_{submenu.pk}" in request.POST,
                    "can_delete": f"can_delete_{submenu.pk}" in request.POST,
                },
            )

        messages.success(request, "Hak akses menu berhasil disimpan.")
        return redirect(f"{self.url_list}?role={selected_role.pk}")
