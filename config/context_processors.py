from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from config.year_options import get_year_options
from menus.models import RolePermission, Menu


SPJ_ACTIVE_SUBMENU_MAP = {
    "penginapan_action": "penginapan_list",
    "penginapan_action_pk": "penginapan_list",
    "penginapan_delete": "penginapan_list",
    "pesawat_action": "pesawat_list",
    "pesawat_action_pk": "pesawat_list",
    "pesawat_delete": "pesawat_list",
    "uang_harian_action": "uang_harian_list",
    "uang_harian_action_pk": "uang_harian_list",
    "uang_harian_delete": "uang_harian_list",
    "transport_action": "transport_list",
    "transport_action_pk": "transport_list",
    "transport_delete": "transport_list",
    "uang_representasi_action": "uang_representasi_list",
    "uang_representasi_action_pk": "uang_representasi_list",
    "uang_representasi_delete": "uang_representasi_list",
    "laporan_perjalanan_action": "laporan_perjalanan_list",
    "laporan_perjalanan_action_pk": "laporan_perjalanan_list",
    "laporan_perjalanan_delete": "laporan_perjalanan_list",
    "laporan_perjalanan_preview": "laporan_perjalanan_list",
    "laporan_perjalanan_print": "laporan_perjalanan_list",
    "kwitansi_print": "kwitansi_list",
}


def _active_submenu_name(request):
    resolver_match = getattr(request, "resolver_match", None)
    url_name = getattr(resolver_match, "url_name", "") or ""
    for suffix in ("_add", "_update", "_delete"):
        if url_name.endswith(suffix):
            return f"{url_name[:-len(suffix)]}_list"
    return SPJ_ACTIVE_SUBMENU_MAP.get(url_name, url_name)


def _resolve_submenu_url(submenu):
    if not submenu.url_name:
        return "#"

    try:
        return reverse(submenu.url_name)
    except NoReverseMatch:
        return "#"


def _prepare_submenus(submenus):
    prepared = []
    for submenu in submenus:
        submenu.resolved_url = _resolve_submenu_url(submenu)
        prepared.append(submenu)
    return prepared


def _get_user_profile(user):
    try:
        return user.userprofile
    except Exception:
        return None


def _get_user_role(user):
    if not getattr(user, "is_authenticated", False):
        return None

    if user.is_superuser:
        return "Superuser"

    profile = _get_user_profile(user)
    role = getattr(profile, "role", None)
    return role.nama if role else "Belum memiliki role"


def _get_active_year(request):
    current_year = timezone.localdate().year
    year = request.session.get("active_year", current_year)

    try:
        return int(year)
    except (TypeError, ValueError):
        return current_year


def user_navigation_context(request):
    active_year = _get_active_year(request)

    context = {
        "active_year": active_year,
        "year_options": get_year_options(extra_year=active_year),
    }

    if request.user.is_authenticated:
        full_name = request.user.get_full_name().strip()
        context.update({
            "active_user_name": full_name or request.user.get_username(),
            "active_user_role": _get_user_role(request.user),
        })

    return context

def menu_context(request):
    context = user_navigation_context(request)

    # Jika belum login → tidak tampilkan menu
    if not request.user.is_authenticated:
        return context

    user = request.user

    # ==============================
    # SUPERUSER (LIHAT SEMUA MENU)
    # ==============================
    if user.is_superuser:
        menus = Menu.objects.filter(aktif=True).prefetch_related('submenus').all()

        menu_data = []
        for menu in menus:
            submenus = _prepare_submenus(menu.submenus.filter(aktif=True))
            if not submenus:
                continue

            menu_data.append({
                'menu': menu,
                'submenus': submenus
            })

        context.update({
            'menu_data': menu_data,
            'active_submenu': _active_submenu_name(request),
        })
        return context

    # ==============================
    # USER BIASA (BERDASARKAN ROLE)
    # ==============================
    try:
        role = user.userprofile.role
    except Exception:
        return context

    if not role:
        return context

    # Ambil permission sesuai role
    permissions = RolePermission.objects.filter(
        role=role,
        can_view=True,
        submenu__aktif=True,
        submenu__menu__aktif=True,
    ).select_related('submenu__menu').order_by(
        'submenu__menu__urutan',
        'submenu__urutan'
    )

    menu_dict = {}

    for perm in permissions:
        menu = perm.submenu.menu

        # Jika menu belum ada → buat
        if menu.id not in menu_dict:
            menu_dict[menu.id] = {
                'menu': menu,
                'submenus': []
            }

        perm.submenu.resolved_url = _resolve_submenu_url(perm.submenu)
        menu_dict[menu.id]['submenus'].append(perm.submenu)

    # Convert ke list
    menu_data = list(menu_dict.values())

    context.update({
        'menu_data': menu_data,
        'active_submenu': _active_submenu_name(request),
    })
    return context
