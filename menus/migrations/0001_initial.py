from django.db import migrations, models
import django.db.models.deletion


def seed_default_menus(apps, schema_editor):
    Menu = apps.get_model("menus", "Menu")
    SubMenu = apps.get_model("menus", "SubMenu")

    master_menu, _ = Menu.objects.update_or_create(
        nama="Data Master",
        defaults={
            "icon": "ti ti-database",
            "urutan": 10,
            "aktif": True,
        },
    )

    SubMenu.objects.update_or_create(
        menu=master_menu,
        nama="OPD",
        defaults={
            "url": "/opd/",
            "url_name": "opd_list",
            "icon": "ti ti-building",
            "urutan": 10,
            "aktif": True,
        },
    )

    SubMenu.objects.update_or_create(
        menu=master_menu,
        nama="Sub OPD",
        defaults={
            "url": "/sub-opd/",
            "url_name": "subopd_list",
            "icon": "ti ti-building-community",
            "urutan": 20,
            "aktif": True,
        },
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=100)),
                ("icon", models.CharField(default="ti ti-folder", max_length=60)),
                ("urutan", models.PositiveIntegerField(default=0)),
                ("aktif", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Menu",
                "verbose_name_plural": "Menu",
                "ordering": ["urutan", "nama"],
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=100, unique=True)),
                ("keterangan", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Role",
                "verbose_name_plural": "Role",
                "ordering": ["nama"],
            },
        ),
        migrations.CreateModel(
            name="SubMenu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=100)),
                ("url", models.CharField(max_length=255)),
                ("url_name", models.CharField(blank=True, max_length=100)),
                ("icon", models.CharField(blank=True, max_length=60)),
                ("urutan", models.PositiveIntegerField(default=0)),
                ("aktif", models.BooleanField(default=True)),
                ("menu", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submenus", to="menus.menu")),
            ],
            options={
                "verbose_name": "Sub Menu",
                "verbose_name_plural": "Sub Menu",
                "ordering": ["menu__urutan", "urutan", "nama"],
                "unique_together": {("menu", "nama")},
            },
        ),
        migrations.CreateModel(
            name="RolePermission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("can_view", models.BooleanField(default=True)),
                ("can_add", models.BooleanField(default=False)),
                ("can_edit", models.BooleanField(default=False)),
                ("can_delete", models.BooleanField(default=False)),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="permissions", to="menus.role")),
                ("submenu", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="permissions", to="menus.submenu")),
            ],
            options={
                "verbose_name": "Hak Akses Menu",
                "verbose_name_plural": "Hak Akses Menu",
                "ordering": ["role__nama", "submenu__menu__urutan", "submenu__urutan"],
                "unique_together": {("role", "submenu")},
            },
        ),
        migrations.RunPython(seed_default_menus, migrations.RunPython.noop),
    ]
