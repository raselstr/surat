from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0002_seed_menu_crud"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submenu",
            name="url",
        ),
    ]
