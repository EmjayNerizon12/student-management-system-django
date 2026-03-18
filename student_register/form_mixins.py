from django import forms


class StyledFieldsMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css_class}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)
