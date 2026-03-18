from django.contrib.auth.models import AbstractUser
from django.db import models


class Degree(models.Model):
    degree_title = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["degree_title"]

    def __str__(self):
        return self.degree_title


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STUDENT = "student", "Student"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        NON_BINARY = "non_binary", "Non-binary"
        PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"

    class YearLevel(models.TextChoices):
        FIRST = "1st Year", "1st Year"
        SECOND = "2nd Year", "2nd Year"
        THIRD = "3rd Year", "3rd Year"
        FOURTH = "4th Year", "4th Year"
        FIFTH = "5th Year", "5th Year"
        GRADUATE = "Graduate", "Graduate"

    class EnrollmentStatus(models.TextChoices):
        ENROLLED = "enrolled", "Enrolled"
        REGULAR = "regular", "Regular"
        ON_LEAVE = "on_leave", "On Leave"
        GRADUATED = "graduated", "Graduated"
        WITHDRAWN = "withdrawn", "Withdrawn"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    student_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default="Philippines")
    degree = models.ForeignKey(
        Degree,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    admission_date = models.DateField(null=True, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    year_level = models.CharField(max_length=20, choices=YearLevel.choices, blank=True)
    section = models.CharField(max_length=50, blank=True)
    enrollment_status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ENROLLED,
    )
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_relationship = models.CharField(max_length=50, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        ordering = ["first_name", "last_name", "username"]

    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_staff:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser or self.is_staff

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(part for part in parts if part).strip() or self.username

    @property
    def full_address(self):
        parts = [self.address_line, self.city, self.state_province, self.postal_code, self.country]
        return ", ".join(part for part in parts if part)
