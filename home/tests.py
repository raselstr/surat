from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from opd.models import OPD, SubOPD


class AdminDashboardTests(TestCase):
    def test_superuser_root_redirects_to_admin_dashboard(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("admin:index"))

    def test_opd_models_are_registered_in_admin(self):
        self.assertIn(OPD, admin.site._registry)
        self.assertIn(SubOPD, admin.site._registry)
