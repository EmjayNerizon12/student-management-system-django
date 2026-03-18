from .decorators import admin_required
from .views_admin import (
    admin_dashboard,
    degree_delete,
    degree_edit,
    degree_list,
    student_create,
    student_delete,
    student_detail,
    student_edit,
    student_list,
)
from .views_auth import dashboard, home, login_view, logout_view
from .views_student import profile, student_dashboard

__all__ = [
    "admin_dashboard",
    "admin_required",
    "dashboard",
    "degree_delete",
    "degree_edit",
    "degree_list",
    "home",
    "login_view",
    "logout_view",
    "profile",
    "student_create",
    "student_dashboard",
    "student_delete",
    "student_detail",
    "student_edit",
    "student_list",
]
