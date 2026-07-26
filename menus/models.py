from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import NoReverseMatch, reverse
from django.dispatch import receiver


class Role(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    keterangan = models.TextField(blank=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Role"
        ordering = ["nama"]

    def __str__(self):
        return self.nama


class Menu(models.Model):
    nama = models.CharField(max_length=100)
    icon = models.CharField(max_length=60, default="ti ti-folder")
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"
        ordering = ["urutan", "nama"]

    def __str__(self):
        return self.nama


class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="submenus")
    nama = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=60, blank=True)
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sub Menu"
        verbose_name_plural = "Sub Menu"
        ordering = ["menu__urutan", "urutan", "nama"]
        unique_together = ("menu", "nama")

    def __str__(self):
        return self.nama

    def get_url(self):
        if not self.url_name:
            return "#"

        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return "#"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    submenu = models.ForeignKey(SubMenu, on_delete=models.CASCADE, related_name="permissions")
    can_view = models.BooleanField(default=True)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Hak Akses Menu"
        verbose_name_plural = "Hak Akses Menu"
        unique_together = ("role", "submenu")
        ordering = ["role__nama", "submenu__menu__urutan", "submenu__urutan"]

    def __str__(self):
        return f"{self.role} - {self.submenu}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="userprofile",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_profiles",
    )

    class Meta:
        verbose_name = "Profil User"
        verbose_name_plural = "Profil User"
        ordering = ["user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
