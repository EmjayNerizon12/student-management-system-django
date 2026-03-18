from django import forms
from django.contrib.auth.forms import UserCreationForm

from .form_mixins import StyledFieldsMixin
from .models import Degree, User


STUDENT_ACCOUNT_FIELDS = (
    "username",
    "email",
    "first_name",
    "middle_name",
    "last_name",
    "student_no",
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
    "degree",
    "admission_date",
    "academic_year",
    "year_level",
    "section",
    "enrollment_status",
    "guardian_name",
    "guardian_relationship",
    "guardian_phone",
    "emergency_contact_name",
    "emergency_contact_relationship",
    "emergency_contact_phone",
    "notes",
    "is_active",
)


class DegreeForm(StyledFieldsMixin, forms.ModelForm):
    class Meta:
        model = Degree
        fields = ("degree_title",)
        labels = {"degree_title": "Degree name"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class StudentAccountCreateForm(StyledFieldsMixin, UserCreationForm):
    class Meta:
        model = User
        fields = STUDENT_ACCOUNT_FIELDS
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["middle_name"].required = False
        self.fields["student_no"].required = True
        self.fields["degree"].required = True
        self.fields["username"].help_text = "Unique login name for the student account."
        self.fields["academic_year"].help_text = "Example: 2026-2027"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        user.is_staff = False
        if commit:
            user.save()
        return user


class StudentAccountUpdateForm(StyledFieldsMixin, forms.ModelForm):
    password = forms.CharField(
        label="New password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Leave blank to keep the current password.",
    )

    class Meta:
        model = User
        fields = STUDENT_ACCOUNT_FIELDS
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["middle_name"].required = False
        self.fields["student_no"].required = True
        self.fields["degree"].required = True
        self.fields["academic_year"].help_text = "Example: 2026-2027"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
