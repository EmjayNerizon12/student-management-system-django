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

PROFILE_FIELD_SECTIONS = (
    {
        "kicker": "Section 01",
        "title": "Personal Identity",
        "description": "Core identity details that describe who you are in the student record.",
        "fields": (
            ("first_name", "col-md-4"),
            ("middle_name", "col-md-4"),
            ("last_name", "col-md-4"),
            ("email", "col-md-6"),
            ("date_of_birth", "col-md-3"),
            ("birth_place", "col-md-6"),
            ("gender", "col-md-3"),
            ("nationality", "col-md-4"),
        ),
    },
    {
        "kicker": "Section 02",
        "title": "Contact Information",
        "description": "Use current contact and address details so the school can reach you easily.",
        "fields": (
            ("phone_number", "col-md-4"),
            ("country", "col-md-4"),
            ("postal_code", "col-md-4"),
            ("address_line", "col-12"),
            ("city", "col-md-4"),
            ("state_province", "col-md-4"),
        ),
    },
    {
        "kicker": "Section 03",
        "title": "Guardian and Emergency Contacts",
        "description": "Trusted contacts to use for support, verification, and urgent situations.",
        "fields": (
            ("guardian_name", "col-md-6"),
            ("guardian_relationship", "col-md-3"),
            ("guardian_phone", "col-md-3"),
            ("emergency_contact_name", "col-md-6"),
            ("emergency_contact_relationship", "col-md-3"),
            ("emergency_contact_phone", "col-md-3"),
        ),
    },
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
