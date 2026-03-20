from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from .models import Degree, User
from .management.commands.seed_admin import DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_USERNAME


class AccountFlowTests(TestCase):
    def setUp(self):
        self.degree = Degree.objects.create(degree_title="Computer Science")
        self.admin_user = User.objects.create_user(
            username="admin01",
            password="admin-pass-123",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="student01",
            password="student-pass-123",
            email="student@example.com",
            first_name="Student",
            last_name="User",
            role=User.Role.STUDENT,
            student_no="STU-001",
            degree=self.degree,
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_student_list(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)

    def test_student_list_is_paginated(self):
        for index in range(2, 14):
            User.objects.create_user(
                username=f"student{index:02d}",
                password="student-pass-123",
                email=f"student{index:02d}@example.com",
                first_name=f"Student{index:02d}",
                last_name="User",
                role=User.Role.STUDENT,
                student_no=f"STU-{index:03d}",
                degree=self.degree,
            )

        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Page 2 of 2")
        self.assertContains(response, "student13@example.com")

    def test_student_is_redirected_from_admin_page(self):
        self.client.login(username="student01", password="student-pass-123")
        response = self.client.get(reverse("student_list"))
        self.assertRedirects(response, reverse("student_dashboard"))

    def test_student_can_view_student_dashboard(self):
        self.client.login(username="student01", password="student-pass-123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_admin_create_student_page_loads(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_create"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_view_student_detail(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_detail", args=[self.student_user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_student_create_success_shows_feedback_modal(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.post(
            reverse("student_create"),
            {
                "username": "student02",
                "email": "student02@example.com",
                "first_name": "Jane",
                "middle_name": "",
                "last_name": "Doe",
                "student_no": "STU-002",
                "degree": self.degree.pk,
                "academic_year": "2025-2026",
                "year_level": User.YearLevel.FIRST,
                "section": "A",
                "enrollment_status": User.EnrollmentStatus.ENROLLED,
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "is_active": "on",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "statusFeedbackModal")
        self.assertContains(response, "Student account created successfully.")

    def test_student_create_invalid_post_shows_error_feedback_modal(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.post(
            reverse("student_create"),
            {
                "username": "",
                "email": "bad-email",
                "first_name": "",
                "last_name": "",
                "student_no": "",
                "password1": "short",
                "password2": "different",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "statusFeedbackModal")
        self.assertContains(response, "Review the highlighted fields and try again.")

    def test_degree_seeder_creates_records(self):
        Degree.objects.all().delete()
        call_command("seed_degrees")
        self.assertGreater(Degree.objects.count(), 0)

    def test_student_seeder_creates_requested_records(self):
        User.objects.filter(role=User.Role.STUDENT).delete()
        call_command("seed_students", count=5, password="SeedPass123!")
        self.assertEqual(User.objects.filter(role=User.Role.STUDENT).count(), 5)

    def test_admin_seeder_creates_default_admin_account(self):
        User.objects.filter(username=DEFAULT_ADMIN_USERNAME).delete()
        call_command("seed_admin")
        admin_user = User.objects.get(username=DEFAULT_ADMIN_USERNAME)
        self.assertEqual(admin_user.email, DEFAULT_ADMIN_EMAIL)
        self.assertEqual(admin_user.role, User.Role.ADMIN)
        self.assertTrue(admin_user.is_staff)

    def test_student_seeder_also_ensures_default_admin_account(self):
        User.objects.filter(username=DEFAULT_ADMIN_USERNAME).delete()
        call_command("seed_students", count=1, password="SeedPass123!")
        self.assertTrue(User.objects.filter(username=DEFAULT_ADMIN_USERNAME, role=User.Role.ADMIN).exists())
