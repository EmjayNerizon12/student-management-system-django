from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("students/new/", views.student_create, name="student_create"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("degrees/", views.degree_list, name="degree_list"),
    path("degrees/<int:pk>/edit/", views.degree_edit, name="degree_edit"),
    path("degrees/<int:pk>/delete/", views.degree_delete, name="degree_delete"),
    path("profile/", views.profile, name="profile"),
]
