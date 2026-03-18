from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_admin_role:
            messages.error(request, "That page is only available to admin accounts.")
            return redirect("student_dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
