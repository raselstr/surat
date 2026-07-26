from django.test import TestCase
from django.urls import reverse

from opd.models import OPD, SubOPD

from .models import Pegawai


class PegawaiCRUDTests(TestCase):
    def setUp(self):
        self.opd = OPD.objects.create(kode="1.01", nama="Dinas Pendidikan")
        self.sub_opd = SubOPD.objects.create(
            kode="1.01.01",
            nama="Sekretariat",
            opd=self.opd,
        )

    def test_list_renders_crud_controls(self):
        response = self.client.get(reverse("pegawai_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tambah")
        self.assertContains(response, "per_page")
        self.assertContains(response, "crudModal")

    def test_create_pegawai_from_add_url(self):
        response = self.client.post(
            reverse("pegawai_add"),
            {
                "nip": "199001012020121001",
                "nama": "Budi Santoso",
                "sub_opd": self.sub_opd.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Pegawai.objects.filter(
                nip="199001012020121001",
                nama="Budi Santoso",
                sub_opd=self.sub_opd,
            ).exists()
        )

    def test_update_pegawai_from_form_url(self):
        pegawai = Pegawai.objects.create(
            nip="199001012020121001",
            nama="Nama Lama",
            sub_opd=self.sub_opd,
        )

        response = self.client.post(
            reverse("pegawai_update", args=[pegawai.pk]),
            {
                "nip": "199001012020121002",
                "nama": "Nama Baru",
                "sub_opd": self.sub_opd.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        pegawai.refresh_from_db()
        self.assertEqual(pegawai.nip, "199001012020121002")
        self.assertEqual(pegawai.nama, "Nama Baru")

    def test_delete_pegawai(self):
        pegawai = Pegawai.objects.create(
            nip="199001012020121001",
            nama="Budi Santoso",
            sub_opd=self.sub_opd,
        )

        response = self.client.post(reverse("pegawai_delete", args=[pegawai.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pegawai.objects.filter(pk=pegawai.pk).exists())
