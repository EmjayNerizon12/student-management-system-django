from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_required
from .forms_admin import DegreeForm, StudentAccountCreateForm, StudentAccountUpdateForm
from .models import Degree, User


@login_required
@admin_required
def admin_dashboard(request):
    students = User.objects.filter(role=User.Role.STUDENT).select_related("degree")
    context = {
        "total_students": students.count(),
        "active_students": students.filter(is_active=True).count(),
        "degree_count": Degree.objects.count(),
        "graduated_students": students.filter(enrollment_status=User.EnrollmentStatus.GRADUATED).count(),
        "recent_students": students.order_by("-date_joined")[:5],
    }
    return render(request, "student_register/admin_dashboard.html", context)


@login_required
@admin_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    students = User.objects.filter(role=User.Role.STUDENT).select_related("degree")
    if query:
        students = students.filter(
            Q(username__icontains=query)
            | Q(student_no__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(degree__degree_title__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(section__icontains=query)
            | Q(enrollment_status__icontains=query)
        )

    context = {
        "students": students.order_by("first_name", "last_name"),
        "query": query,
    }
    return render(request, "student_register/student_list.html", context)


@login_required
@admin_required
def student_detail(request, pk):
    student = get_object_or_404(User.objects.select_related("degree"), pk=pk, role=User.Role.STUDENT)
    return render(request, "student_register/student_detail.html", {"student": student})


@login_required
@admin_required
def student_create(request):
    form = StudentAccountCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student account created successfully.")
        return redirect("student_list")
    return render(
        request,
        "student_register/student_form.html",
        {"form": form, "page_title": "Create Student Account", "submit_label": "Create account"},
    )


@login_required
@admin_required
def student_edit(request, pk):
    student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
    form = StudentAccountUpdateForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student account updated successfully.")
        return redirect("student_list")
    return render(
        request,
        "student_register/student_form.html",
        {"form": form, "page_title": "Edit Student Account", "submit_label": "Save changes", "student": student},
    )


@login_required
@admin_required
def student_delete(request, pk):
    student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student account removed.")
    return redirect("student_list")


@login_required
@admin_required
def degree_list(request):
    form = DegreeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Degree added successfully.")
        return redirect("degree_list")

    context = {
        "form": form,
        "degrees": Degree.objects.prefetch_related("students").all(),
    }
    return render(request, "student_register/degree_list.html", context)


@login_required
@admin_required
def degree_edit(request, pk):
    degree = get_object_or_404(Degree, pk=pk)
    form = DegreeForm(request.POST or None, instance=degree)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Degree updated successfully.")
        return redirect("degree_list")
    return render(
        request,
        "student_register/degree_form.html",
        {"form": form, "page_title": "Edit Degree", "submit_label": "Save degree"},
    )


@login_required
@admin_required
def degree_delete(request, pk):
    degree = get_object_or_404(Degree, pk=pk)
    if request.method == "POST":
        degree.delete()
        messages.success(request, "Degree removed.")
    return redirect("degree_list")
