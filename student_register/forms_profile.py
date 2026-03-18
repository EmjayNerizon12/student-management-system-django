from django import forms

from .form_mixins import StyledFieldsMixin
from .models import User


PROFILE_FIELDS = (
    "first_name",
    "middle_name",
    "last_name",
    "email",
    "date_of_birth",
    "birth_place",
    "gender",
    "nationality",
    "phone_number",
    "address_line",
    "city",
    "state_province",
    "postal_code",
    "country",
    "guardian_name",
    "guardian_relationship",
    "guardian_phone",
    "emergency_contact_name",
    "emergency_contact_relationship",
    "emergency_contact_phone",
)


class ProfileForm(StyledFieldsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = PROFILE_FIELDS
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["middle_name"].required = False
