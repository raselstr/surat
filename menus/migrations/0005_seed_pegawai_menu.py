from django.db import migrations


def seed_pegawai_menu(apps, schema_editor):
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
        nama="Pegawai",
        defaults={
            "url_name": "pegawai_list",
            "icon": "ti ti-id-badge-2",
            "urutan": 30,
            "aktif": True,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0004_userprofile"),
    ]

    operations = [
        migrations.RunPython(seed_pegawai_menu, migrations.RunPython.noop),
    ]
