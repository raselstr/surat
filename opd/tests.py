from django.test import TestCase
from django.urls import reverse

from .models import OPD, SubOPD


class OPDCRUDTests(TestCase):
    def test_list_renders_universal_crud_controls(self):
        response = self.client.get(reverse("opd_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Import")
        self.assertContains(response, "Export")
        self.assertContains(response, "Tambah")
        self.assertContains(response, "per_page")
        self.assertContains(response, "crudModal")

    def test_create_opd_from_add_url(self):
        response = self.client.post(
            reverse("opd_add"),
            {"kode": "1.01", "nama": "Dinas Pendidikan"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(OPD.objects.filter(kode="1.01", nama="Dinas Pendidikan").exists())

    def test_update_opd_from_form_url(self):
        opd = OPD.objects.create(kode="1.01", nama="Nama Lama")

        response = self.client.post(
            reverse("opd_update", args=[opd.pk]),
            {"kode": "1.02", "nama": "Nama Baru"},
        )

        self.assertEqual(response.status_code, 302)
        opd.refresh_from_db()
        self.assertEqual(opd.kode, "1.02")
        self.assertEqual(opd.nama, "Nama Baru")

    def test_update_form_renders_for_modal(self):
        opd = OPD.objects.create(kode="1.01", nama="Nama Lama")

        response = self.client.get(
            reverse("opd_update", args=[opd.pk]),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hx-post")
        self.assertNotContains(response, "data-confirm=\"save\"")

    def test_delete_opd(self):
        opd = OPD.objects.create(kode="1.01", nama="Dinas Pendidikan")

        response = self.client.post(reverse("opd_delete", args=[opd.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(OPD.objects.filter(pk=opd.pk).exists())


class SubOPDCRUDTests(TestCase):
    def test_create_subopd_from_add_url(self):
        opd = OPD.objects.create(kode="1.01", nama="Dinas Pendidikan")

        response = self.client.post(
            reverse("subopd_add"),
            {"kode": "1.01.01", "nama": "Sekretariat", "opd": opd.pk},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            SubOPD.objects.filter(kode="1.01.01", nama="Sekretariat", opd=opd).exists()
        )
