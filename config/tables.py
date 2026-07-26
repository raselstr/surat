import django_tables2 as tables
from django.utils.html import format_html
from config.utils.formatting import format_indonesian_number, is_money_identifier


def action_column(update_url_name, delete_url_name):
    return tables.TemplateColumn(
        template_name="components/crud/aksi.html",
        extra_context={
            "update_url_name": update_url_name,
            "delete_url_name": delete_url_name,
        },
        orderable=False,
        verbose_name="Aksi",
    )


def _append_css_class(attrs, section, class_name):
    section_attrs = attrs.setdefault(section, {})
    existing_classes = section_attrs.get("class", "").split()

    if class_name not in existing_classes:
        existing_classes.append(class_name)

    section_attrs["class"] = " ".join(filter(None, existing_classes))


def render_numbered_list(queryset, attr_name):
    """
    Menampilkan data sebagai daftar bernomor (ordered list)

    Contoh:
    render_numbered_list(record.pelaksana.all(), "nama")
    """

    if not queryset.exists():
        return "-"

    items = "".join([
        f"<li>{getattr(item, attr_name, '-')}</li>"
        for item in queryset
    ])

    return format_html(
        '<ol style="margin:0; padding-left:20px; text-align:left;">{}</ol>',
        format_html(items)
    )

class BaseTable(tables.Table):
    no = tables.Column(
        empty_values=(),
        verbose_name="No",
        orderable=False,
        attrs={
            "th": {"class": "text-start", "style": "width: 56px;"},
            "td": {"class": "text-start"},
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_money_columns()

    def _configure_money_columns(self):
        for name, bound_column in self.columns.items():
            if not is_money_identifier(name):
                continue

            column = bound_column.column
            attrs = column.attrs or {}
            column.attrs = attrs

            _append_css_class(attrs, "th", "text-end")
            _append_css_class(attrs, "td", "text-end")

    def __getattr__(self, attr_name):
        if attr_name.startswith("render_"):
            column_name = attr_name.removeprefix("render_")
            if is_money_identifier(column_name):
                return self._render_money_value

        raise AttributeError(f"{self.__class__.__name__} has no attribute '{attr_name}'")

    def _render_money_value(self, value, **kwargs):
        return format_indonesian_number(value)

    def render_no(self, bound_row):
        table = bound_row.table
        page = getattr(table, "page", None)

        number = bound_row.row_counter + 1

        if page:
            return number + (page.number - 1) * page.paginator.per_page

        return number


    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-hover table-bordered align-middle"
        }
