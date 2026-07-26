from django import forms
from django.contrib.auth import get_user_model

from config.forms import BaseAppModelForm

from .models import Menu, Role, RolePermission, SubMenu, UserProfile


User = get_user_model()


class MenuForm(BaseAppModelForm):
    class Meta:
        model = Menu
        fields = ["nama", "icon", "urutan", "aktif"]


class SubMenuForm(BaseAppModelForm):
    class Meta:
        model = SubMenu
        fields = ["menu", "nama", "url_name", "icon", "urutan", "aktif"]


class RoleForm(BaseAppModelForm):
    class Meta:
        model = Role
        fields = ["nama", "keterangan"]


class RolePermissionForm(BaseAppModelForm):
    class Meta:
        model = RolePermission
        fields = ["role", "submenu", "can_view", "can_add", "can_edit", "can_delete"]


class UserForm(BaseAppModelForm):
    role = forms.ModelChoiceField(
        label="Role",
        queryset=Role.objects.all(),
        required=False,
        help_text="Role menentukan akses menu user.",
    )
    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )
    password2 = forms.CharField(
        label="Konfirmasi Password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            profile = getattr(self.instance, "userprofile", None)
            if profile:
                self.fields["role"].initial = profile.role

        if not self.instance.pk:
            self.fields["password1"].required = True
            self.fields["password2"].required = True

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Password dan konfirmasi password tidak sama.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"role": self.cleaned_data.get("role")},
            )

        return user


class UserSelfProfileForm(BaseAppModelForm):
    password1 = forms.CharField(
        label="Password Baru",
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Kosongkan jika password tidak ingin diubah.",
    )
    password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Password dan konfirmasi password tidak sama.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
