import os

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.db import models

from config.utils.image_compression import compress_if_image, is_uploaded_image
from config.utils.formatting import (
    format_indonesian_number,
    is_money_identifier,
    parse_localized_decimal,
)


INDONESIAN_DATE_INPUT_FORMATS = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]


def append_widget_class(widget, *class_names):
    existing = widget.attrs.get("class", "").split()

    for class_name in class_names:
        if class_name and class_name not in existing:
            existing.append(class_name)

    widget.attrs["class"] = " ".join(existing).strip()


class IndonesianDateInput(forms.DateInput):
    input_type = "text"

    def __init__(self, attrs=None, format=None):
        attrs = attrs or {}
        attrs.setdefault("placeholder", "dd/mm/yyyy")
        super().__init__(attrs=attrs, format=format or "%d/%m/%Y")


class IndonesianDecimalField(forms.DecimalField):
    def __init__(self, *args, integer_only=False, **kwargs):
        self.integer_only = integer_only
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            value = parse_localized_decimal(value)
        except ValueError as exc:
            raise forms.ValidationError("Masukkan angka dengan format yang benar.") from exc

        if self.integer_only and value != value.to_integral_value():
            raise forms.ValidationError("Masukkan bilangan bulat tanpa desimal.")

        return super().to_python(value)

    def prepare_value(self, value):
        return format_indonesian_number(value)


class IndonesianIntegerField(forms.IntegerField):
    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            decimal_value = parse_localized_decimal(value)
        except ValueError as exc:
            raise forms.ValidationError("Masukkan bilangan bulat dengan format yang benar.") from exc

        if decimal_value != decimal_value.to_integral_value():
            raise forms.ValidationError("Masukkan bilangan bulat tanpa desimal.")

        return super().to_python(int(decimal_value))

    def prepare_value(self, value):
        return format_indonesian_number(value)


class IndonesianFloatField(forms.FloatField):
    def __init__(self, *args, integer_only=False, **kwargs):
        self.integer_only = integer_only
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            value = parse_localized_decimal(value)
        except ValueError as exc:
            raise forms.ValidationError("Masukkan angka dengan format yang benar.") from exc

        if self.integer_only and value != value.to_integral_value():
            raise forms.ValidationError("Masukkan bilangan bulat tanpa desimal.")

        return super().to_python(value)

    def prepare_value(self, value):
        return format_indonesian_number(value)


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
        self._apply_localized_fields()
        self._apply_default_widget_styles()

    def _apply_localized_fields(self):
        for name, field in list(self.fields.items()):
            model_field = self._get_model_field(name)

            if isinstance(model_field, models.DateField) and not isinstance(model_field, models.DateTimeField):
                field.input_formats = INDONESIAN_DATE_INPUT_FORMATS
                field.widget = IndonesianDateInput()
                continue

            if self._is_money_model_field(name, model_field):
                self.fields[name] = self._build_money_form_field(field, model_field)

    def _is_money_model_field(self, name, model_field):
        money_field_types = (
            models.DecimalField,
            models.FloatField,
            models.IntegerField,
            models.BigIntegerField,
            models.PositiveBigIntegerField,
            models.PositiveIntegerField,
            models.PositiveSmallIntegerField,
            models.SmallIntegerField,
        )

        return isinstance(model_field, money_field_types) and is_money_identifier(name)

    def _get_common_field_kwargs(self, field):
        return {
            "label": field.label,
            "required": field.required,
            "help_text": field.help_text,
            "initial": field.initial,
            "validators": field.validators,
            "error_messages": field.error_messages,
            "disabled": field.disabled,
        }

    def _build_money_form_field(self, field, model_field):
        kwargs = self._get_common_field_kwargs(field)
        widget_attrs = dict(getattr(field.widget, "attrs", {}) or {})
        widget_attrs.setdefault("inputmode", "decimal")
        widget_attrs.setdefault("autocomplete", "off")
        widget_attrs.setdefault("placeholder", "0")

        if isinstance(model_field, models.DecimalField):
            money_field = IndonesianDecimalField(
                max_digits=model_field.max_digits,
                decimal_places=model_field.decimal_places,
                integer_only=True,
                max_value=getattr(field, "max_value", None),
                min_value=getattr(field, "min_value", None),
                widget=forms.TextInput(attrs=widget_attrs),
                **kwargs,
            )
        elif isinstance(model_field, models.FloatField):
            money_field = IndonesianFloatField(
                integer_only=True,
                max_value=getattr(field, "max_value", None),
                min_value=getattr(field, "min_value", None),
                widget=forms.TextInput(attrs=widget_attrs),
                **kwargs,
            )
        else:
            widget_attrs["inputmode"] = "numeric"
            money_field = IndonesianIntegerField(
                max_value=getattr(field, "max_value", None),
                min_value=getattr(field, "min_value", None),
                widget=forms.TextInput(attrs=widget_attrs),
                **kwargs,
            )

        money_field.widget.attrs["data-localized-number"] = "true"
        money_field.widget.attrs["data-integer-only"] = "true"
        return money_field

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
                widget.attrs.setdefault("placeholder", "dd/mm/yyyy")
                widget.format = "%d/%m/%Y"
                field.input_formats = INDONESIAN_DATE_INPUT_FORMATS
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

                if widget.attrs.get("data-localized-number"):
                    append_widget_class(widget, "localized-number")

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
