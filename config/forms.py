import os

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.db import models

from config.utils.image_compression import compress_if_image, is_uploaded_image


def append_widget_class(widget, *class_names):
    existing = widget.attrs.get("class", "").split()

    for class_name in class_names:
        if class_name and class_name not in existing:
            existing.append(class_name)

    widget.attrs["class"] = " ".join(existing).strip()


class BaseAppModelForm(forms.ModelForm):
    """
    Form CRUD generik yang bisa dipakai ulang antar app.

    Fitur:
    - styling widget default bootstrap
    - layout kolom fleksibel via `field_layout`
    - metadata file existing untuk preview pada template generik
    """

    accepts_request = True
    field_layout = {}
    default_field_class = "col-md-12"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self._apply_default_widget_styles()

    def _apply_default_widget_styles(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                append_widget_class(widget, "form-check-input")
                continue

            if isinstance(widget, forms.Textarea):
                append_widget_class(widget, "form-control")
                widget.attrs.setdefault("rows", 3)
                continue

            if isinstance(widget, forms.ClearableFileInput):
                append_widget_class(widget, "form-control")
                model_field = self._get_model_field(name)
                if isinstance(model_field, models.ImageField):
                    widget.attrs.setdefault("accept", "image/*")
                continue

            if isinstance(widget, forms.SelectMultiple):
                append_widget_class(widget, "form-select", "select2")
                continue

            if isinstance(widget, forms.Select):
                append_widget_class(widget, "form-select")
                if isinstance(field, forms.ModelChoiceField):
                    append_widget_class(widget, "select2")
                continue

            if isinstance(widget, forms.DateInput):
                append_widget_class(widget, "form-control")
                widget.attrs.setdefault("type", "date")
                widget.format = "%Y-%m-%d"
                field.input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
                continue

            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                ),
            ):
                append_widget_class(widget, "form-control")

    def _get_model_field(self, name):
        try:
            return self._meta.model._meta.get_field(name)
        except Exception:
            return None

    def clean(self):
        cleaned_data = super().clean()

        for name, value in list(cleaned_data.items()):
            if not isinstance(value, UploadedFile) or not is_uploaded_image(value):
                continue

            cleaned_data[name] = compress_if_image(value)

        return cleaned_data

    def get_field_layout(self):
        return getattr(self, "field_layout", {}) or {}

    def get_field_column_class(self, field_name):
        configured = self.get_field_layout().get(field_name)

        if isinstance(configured, int):
            return f"col-md-{configured}"

        if isinstance(configured, str) and configured.strip():
            return configured.strip()

        return self.default_field_class

    @property
    def normalized_field_layout(self):
        return {
            field_name: self.get_field_column_class(field_name)
            for field_name in self.fields.keys()
        }

    @property
    def existing_files(self):
        files = {}

        if not getattr(self.instance, "pk", None):
            return files

        for name in self.fields.keys():
            model_field = self._get_model_field(name)

            if not isinstance(model_field, models.FileField):
                continue

            file_value = getattr(self.instance, name, None)

            if not file_value or not getattr(file_value, "name", ""):
                continue

            try:
                file_url = file_value.url
            except Exception:
                file_url = ""

            files[name] = {
                "name": os.path.basename(file_value.name),
                "url": file_url,
                "is_image": isinstance(model_field, models.ImageField),
            }

        return files
