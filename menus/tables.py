import django_tables2 as tables
from django.contrib.auth import get_user_model

from config.tables import BaseTable, action_column

from .models import Menu, Role, RolePermission, SubMenu


User = get_user_model()


class MenuTable(BaseTable):
    aksi = action_column("menu_update", "menu_delete")

    class Meta(BaseTable.Meta):
        model = Menu
        fields = ("no", "nama", "icon", "urutan", "aktif", "aksi")
        order_by = ("urutan", "nama")


class SubMenuTable(BaseTable):
    aksi = action_column("submenu_update", "submenu_delete")

    class Meta(BaseTable.Meta):
        model = SubMenu
        fields = ("no", "menu", "nama", "url_name", "icon", "urutan", "aktif", "aksi")
        order_by = ("menu__urutan", "urutan", "nama")


class RoleTable(BaseTable):
    aksi = action_column("role_update", "role_delete")

    class Meta(BaseTable.Meta):
        model = Role
        fields = ("no", "nama", "keterangan", "aksi")
        order_by = ("nama",)


class RolePermissionTable(BaseTable):
    aksi = action_column("rolepermission_update", "rolepermission_delete")

    class Meta(BaseTable.Meta):
        model = RolePermission
        fields = ("no", "role", "submenu", "can_view", "can_add", "can_edit", "can_delete", "aksi")
        order_by = ("role__nama", "submenu__menu__urutan", "submenu__urutan")


class UserTable(BaseTable):
    nama_lengkap = tables.Column(
        accessor="get_full_name",
        verbose_name="Nama Lengkap",
        empty_values=(),
    )
    role = tables.Column(
        empty_values=(),
        verbose_name="Role",
        orderable=False,
    )
    aksi = action_column("user_update", "user_delete")

    class Meta(BaseTable.Meta):
        model = User
        fields = (
            "no",
            "username",
            "nama_lengkap",
            "email",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "aksi",
        )
        order_by = ("username",)

    def render_nama_lengkap(self, record):
        return record.get_full_name() or "-"

    def render_role(self, record):
        profile = getattr(record, "userprofile", None)
        role = getattr(profile, "role", None)
        return role.nama if role else "-"
