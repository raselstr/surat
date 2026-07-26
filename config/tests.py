from django.test import SimpleTestCase

from config.crud.base import BaseCRUDView
from config.tables import BaseTable


class DummyTable:
    def __init__(self, queryset, **kwargs):
        self.queryset = queryset
        self.kwargs = kwargs
        self.extra_context = {}


class DummyCRUDView(BaseCRUDView):
    model = type("DummyModel", (), {})
    table_class = DummyTable

    def get_table_kwargs(self, queryset):
        return {"foo": "bar"}


class BaseCRUDViewTests(SimpleTestCase):
    def test_get_table_uses_overridable_kwargs_and_extra_context(self):
        view = DummyCRUDView()
        view.url_list = "/items/"

        table = view.get_table([])

        self.assertIsInstance(table, DummyTable)
        self.assertEqual(table.kwargs["foo"], "bar")
        self.assertEqual(table.extra_context["url_list"], "/items/")
