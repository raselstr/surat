from django.apps import apps
from django.db import DatabaseError
from django.utils import timezone


def normalize_year(value):
    current_year = timezone.localdate().year

    try:
        return int(value)
    except (TypeError, ValueError):
        return current_year


def get_data_years():
    years = set()

    for model in apps.get_models():
        field_names = {
            field.name
            for field in model._meta.get_fields()
            if getattr(field, "concrete", False)
        }

        if "tahun" not in field_names:
            continue

        try:
            values = (
                model.objects
                .exclude(tahun__isnull=True)
                .values_list("tahun", flat=True)
                .distinct()
            )
            for value in values:
                years.add(int(value))
        except (DatabaseError, TypeError, ValueError):
            continue

    return years


def get_year_options(extra_year=None):
    current_year = timezone.localdate().year
    years = set(range(current_year - 3, current_year + 2))
    years.update(get_data_years())

    if extra_year is not None:
        years.add(normalize_year(extra_year))

    return sorted(years, reverse=True)
