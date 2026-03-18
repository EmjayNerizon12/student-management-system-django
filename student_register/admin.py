from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Degree, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "student_no", "degree", "year_level", "enrollment_status", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "degree", "year_level", "enrollment_status", "gender")
    fieldsets = UserAdmin.fieldsets + (
        ("Personal information", {"fields": ("middle_name", "date_of_birth", "birth_place", "gender", "nationality", "phone_number")}),
        ("Address information", {"fields": ("address_line", "city", "state_province", "postal_code", "country")}),
        ("Academic profile", {"fields": ("role", "student_no", "degree", "admission_date", "academic_year", "year_level", "section", "enrollment_status")}),
        ("Guardian and emergency", {"fields": ("guardian_name", "guardian_relationship", "guardian_phone", "emergency_contact_name", "emergency_contact_relationship", "emergency_contact_phone", "notes")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Student profile", {"fields": ("role", "email", "first_name", "last_name", "middle_name", "student_no", "degree", "academic_year", "year_level", "section", "enrollment_status")}),
    )
    search_fields = ("username", "email", "first_name", "last_name", "student_no", "phone_number", "section")
    ordering = ("username",)


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("degree_title",)
    search_fields = ("degree_title",)
