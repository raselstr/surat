from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_existing_user_profiles(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    UserProfile = apps.get_model("menus", "UserProfile")

    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("menus", "0003_remove_submenu_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="user_profiles", to="menus.role")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="userprofile", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Profil User",
                "verbose_name_plural": "Profil User",
                "ordering": ["user__username"],
            },
        ),
        migrations.RunPython(create_existing_user_profiles, migrations.RunPython.noop),
    ]
