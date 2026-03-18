from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms_auth import LoginForm


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_admin_role:
        return redirect("admin_dashboard")
    return redirect("student_dashboard")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "student_register/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    if request.user.is_admin_role:
        return redirect("admin_dashboard")
    return redirect("student_dashboard")
