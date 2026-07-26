from django.db import migrations


def seed_menu_crud(apps, schema_editor):
    Menu = apps.get_model("menus", "Menu")
    SubMenu = apps.get_model("menus", "SubMenu")

    pengaturan_menu, _ = Menu.objects.update_or_create(
        nama="Pengaturan",
        defaults={
            "icon": "ti ti-settings",
            "urutan": 90,
            "aktif": True,
        },
    )

    submenus = [
        {
            "nama": "Menu",
            "url": "/menu/",
            "url_name": "menu_list",
            "icon": "ti ti-menu-2",
            "urutan": 10,
        },
        {
            "nama": "Sub Menu",
            "url": "/sub-menu/",
            "url_name": "submenu_list",
            "icon": "ti ti-list",
            "urutan": 20,
        },
        {
            "nama": "Role",
            "url": "/role/",
            "url_name": "role_list",
            "icon": "ti ti-users",
            "urutan": 30,
        },
        {
            "nama": "Hak Akses Menu",
            "url": "/hak-akses-menu/",
            "url_name": "rolepermission_list",
            "icon": "ti ti-shield-lock",
            "urutan": 40,
        },
    ]

    for submenu in submenus:
        SubMenu.objects.update_or_create(
            menu=pengaturan_menu,
            nama=submenu["nama"],
            defaults={
                "url": submenu["url"],
                "url_name": submenu["url_name"],
                "icon": submenu["icon"],
                "urutan": submenu["urutan"],
                "aktif": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_menu_crud, migrations.RunPython.noop),
    ]
