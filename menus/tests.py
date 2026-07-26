from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from config.context_processors import menu_context
from .models import Menu, SubMenu


class MenuContextTests(TestCase):
    def test_superuser_sees_active_menu_data(self):
        Menu.objects.all().delete()
        menu = Menu.objects.create(nama="Data Master", icon="ti ti-database", urutan=1)
        SubMenu.objects.create(menu=menu, nama="OPD", url="/opd/", url_name="opd_list")
        SubMenu.objects.create(menu=menu, nama="Nonaktif", url="/x/", aktif=False)

        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        request = RequestFactory().get(reverse("opd_list"))
        request.user = user
        request.resolver_match = type("ResolverMatch", (), {"url_name": "opd_list"})()

        context = menu_context(request)

        self.assertEqual(context["active_submenu"], "opd_list")
        self.assertEqual(len(context["menu_data"]), 1)
        self.assertEqual(list(context["menu_data"][0]["submenus"])[0].nama, "OPD")

    def test_menu_crud_pages_render_for_superuser(self):
        user = get_user_model().objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="password",
        )
        self.client.force_login(user)

        for url_name in ("menu_list", "submenu_list", "role_list", "rolepermission_list"):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Tambah")

    def test_active_submenu_maps_crud_action_to_list(self):
        request = RequestFactory().get(reverse("menu_update", args=[1]))
        request.user = get_user_model().objects.create_superuser(
            username="root",
            email="root@example.com",
            password="password",
        )
        request.resolver_match = type("ResolverMatch", (), {"url_name": "menu_update"})()

        context = menu_context(request)

        self.assertEqual(context["active_submenu"], "menu_list")
