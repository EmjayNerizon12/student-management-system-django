from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms_profile import ProfileForm
from .models import User


@login_required
def student_dashboard(request):
    if request.user.is_admin_role:
        return redirect("admin_dashboard")

    degree_peers = 0
    if request.user.degree_id:
        degree_peers = User.objects.filter(
            role=User.Role.STUDENT,
            degree=request.user.degree,
        ).exclude(pk=request.user.pk).count()

    context = {
        "degree_peers": degree_peers,
        "student": request.user,
    }
    return render(request, "student_register/student_dashboard.html", context)


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")

    return render(request, "student_register/profile.html", {"form": form})
