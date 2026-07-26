from django.db.models import Q


GLOBAL_PENANDATANGAN_TASKS = ("Bupati", "Wakil Bupati")
ADMINISTRATOR_GLOBAL_PENANDATANGAN_TASKS = (
    "Bupati",
    "Wakil Bupati",
    "Sekretaris Daerah",
)


def is_administrator_user(user):
    if not user or not getattr(user, "is_authenticated", False):
        return False

    try:
        role_name = user.userprofile.role.nama or ""
    except Exception:
        return False

    return role_name.strip().lower() == "administrator"


def is_administrator_request(request):
    return is_administrator_user(getattr(request, "user", None))


def get_global_penandatangan_tasks(request=None):
    if is_administrator_request(request):
        return ADMINISTRATOR_GLOBAL_PENANDATANGAN_TASKS

    return GLOBAL_PENANDATANGAN_TASKS


def get_active_opd_id(request):
    if not request:
        return None

    user = getattr(request, "user", None)
    if not user or not user.is_authenticated or user.is_superuser:
        return None

    session_opd_id = request.session.get("session_opd_id")
    if session_opd_id:
        return session_opd_id

    try:
        return user.userprofile.opd_id
    except Exception:
        return None


def filter_queryset_by_active_opd(queryset, request, lookup):
    active_opd_id = get_active_opd_id(request)
    if not active_opd_id:
        return queryset

    return queryset.filter(**{lookup: active_opd_id})


def filter_penandatangan_queryset(
    queryset,
    request,
    opd_lookup="opd_id",
    include_global_tasks=True,
    exclude_tasks=None,
):
    active_opd_id = get_active_opd_id(request)
    result_queryset = queryset

    if active_opd_id:
        filters = Q(**{opd_lookup: active_opd_id})

        if include_global_tasks:
            filters |= Q(tugas__in=get_global_penandatangan_tasks(request))

        result_queryset = queryset.filter(filters).distinct()

    if exclude_tasks:
        result_queryset = result_queryset.exclude(tugas__in=exclude_tasks)

    return result_queryset
